#!/usr/bin/env python3
"""Inventory supplied HTTP scenarios faithfully; never invent test expectations."""
import argparse
import json
import re
import shlex
import zipfile
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

try:
    import yaml
except ImportError:
    yaml = None

METHODS = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'}


def _url_path(url):
    if re.match(r'^https?://', url, re.I):
        parts = urlsplit(url)
        return (parts.path or '/') + ('?' + parts.query if parts.query else '')
    # A leading base URL variable is distinct from resource-path variables.
    match = re.match(r'^(\{\{[^{}]+\}\}|\$\{[^{}]+\})(.*)$', url)
    if match:
        suffix = match.group(2)
        return suffix if suffix.startswith('/') else '/' + suffix
    if url.startswith('/'):
        return url.split('#', 1)[0]
    raise ValueError('URL needs an HTTP origin, base URL variable, or resource path')


def _append_endpoint(out, method, path, source, **extra):
    method = method.upper().strip()
    if method not in METHODS or not path:
        raise ValueError('Unsupported or incomplete HTTP endpoint')
    out.append({'method': method, 'path': path, 'source': source, **extra})


def _body_fields(raw, headers):
    if raw is None:
        return {}
    content_type = next((v for k, v in headers.items() if k.lower() == 'content-type'), '')
    if 'json' in content_type.lower():
        try:
            return {'body': json.loads(raw), 'body_encoding': 'json'}
        except (ValueError, TypeError):
            pass  # Malformed payloads can be legitimate negative-test inputs.
    return {'body': raw, 'body_encoding': 'raw'}


def _parse_curl(text, source):
    out = []
    for line in text.replace('\\\n', ' ').splitlines():
        tokens = shlex.split(line, comments=True)
        if not tokens or 'curl' not in tokens:
            continue
        tokens = tokens[tokens.index('curl') + 1:]
        method, url, headers, data = None, None, {}, []
        use_get, use_head, input_files, unsupported = False, False, [], []
        index = 0
        while index < len(tokens):
            token = tokens[index]; index += 1
            option, equal, attached = token.partition('=')
            if token.startswith('-X') and token != '-X': option, equal, attached = '-X', '=', token[2:]
            if token.startswith('-H') and token != '-H': option, equal, attached = '-H', '=', token[2:]
            if token.startswith('-d') and token != '-d': option, equal, attached = '-d', '=', token[2:]
            if option in ('-X','--request','--url','-H','--header','-d','--data','--data-raw','--data-binary','--data-urlencode','--json','-F','--form','-T','--upload-file'):
                if equal: value = attached
                else:
                    if index >= len(tokens): raise ValueError('Missing curl option value: ' + option)
                    value = tokens[index]; index += 1
                if option in ('-X','--request'): method = value.upper()
                elif option == '--url': url = value
                elif option in ('-H','--header'):
                    key, sep, val = value.partition(':')
                    if not sep: raise ValueError('Unsupported curl header syntax')
                    headers[key.strip()] = val.strip()
                elif option in ('-F','--form','-T','--upload-file'):
                    input_files.append({'option':option,'value':value})
                else:
                    if value.startswith('@') and option not in ('--data-raw','--json'):
                        input_files.append({'option':option,'value':value})
                    else: data.append(value)
                    if option == '--json':
                        headers.setdefault('Content-Type','application/json');headers.setdefault('Accept','application/json')
                    elif option == '--data-urlencode':
                        unsupported.append('data-urlencode requires encoding review')
            elif token in ('-G','--get'): use_get = True
            elif token in ('-I','--head'): use_head = True
            elif token.startswith(('http://','https://','{{','${','/')): url = token
            elif token.startswith('-'): unsupported.append(token)
        if not url: raise ValueError('curl URL is missing')
        default_method = 'HEAD' if use_head else ('GET' if use_get else ('PUT' if any(x['option'] in ('-T','--upload-file') for x in input_files) else ('POST' if data or input_files else 'GET')))
        method = method or default_method
        if data and not use_get: headers.setdefault('Content-Type','application/x-www-form-urlencoded')
        path = _url_path(url)
        raw = '&'.join(data) if data else None
        if use_get and raw is not None:
            path += ('&' if '?' in path else '?') + raw; raw = None
        extra = {'raw_url':url,'format':'curl','headers':headers,**_body_fields(raw,headers)}
        if input_files: extra['unresolved_input_files'] = input_files
        if unsupported: extra['review_required'] = unsupported
        _append_endpoint(out,method,path,source,**extra)
    return out


def _parse_postman(obj, source):
    out = []
    def walk(items):
        for item in items or []:
            req = item.get('request')
            if isinstance(req,dict):
                url = req.get('url','')
                if isinstance(url,dict):
                    raw_url = url.get('raw')
                    if raw_url: path = _url_path(raw_url)
                    elif isinstance(url.get('path'),list): path = '/' + '/'.join(str(p) for p in url['path'])
                    else: raise ValueError('Postman request URL is missing')
                else: raw_url = url; path = _url_path(url)
                headers = {h['key']:h.get('value','') for h in req.get('header',[]) if h.get('key') and not h.get('disabled')}
                body = req.get('body',{})
                fields = _body_fields(body.get('raw'),headers) if body.get('mode')=='raw' else {}
                if body and body.get('mode')!='raw': fields['unresolved_body'] = body
                _append_endpoint(out,req.get('method','GET'),path,source,raw_url=raw_url,format='postman',headers=headers,**fields)
            if isinstance(item.get('item'),list): walk(item['item'])
    walk(obj.get('item',[]))
    return out


def _resolve(value, document, seen=()):
    if not isinstance(value,dict) or '$ref' not in value: return value
    ref = value['$ref']
    if not isinstance(ref,str) or not ref.startswith('#/') or ref in seen: return value
    resolved = document
    try:
        for key in ref[2:].split('/'): resolved = resolved[key.replace('~1','/').replace('~0','~')]
    except (KeyError,TypeError): return value
    return _resolve(resolved,document,(*seen,ref))


def _parse_openapi(obj, source):
    out = []
    for path, item in obj.get('paths',{}).items():
        item = _resolve(item,obj)
        for key, operation in item.items():
            method = key.upper()
            if method not in METHODS: continue
            operation = _resolve(operation,obj)
            request = _resolve(operation.get('requestBody',{}),obj)
            content = request.get('content',{})
            media_type = 'application/json' if 'application/json' in content else next(iter(content),'')
            media = content.get(media_type,{})
            fields = {'format':'openapi','headers':{'Content-Type':media_type} if media_type else {},
                      'body_required':bool(request.get('required')), 'parameters':item.get('parameters',[]) + operation.get('parameters',[])}
            if 'security' in operation:
                security_requirements = operation['security']
                security_scope = 'operation'
            else:
                security_requirements = obj.get('security', [])
                security_scope = 'root'
            if not isinstance(security_requirements, list):
                fields['review_required'] = [f'malformed OpenAPI {security_scope} security must be an array']
            elif security_requirements:
                fields['security_requirements'] = security_requirements
                if any(not isinstance(alternative, dict) for alternative in security_requirements) or any(
                        not isinstance(name, str) or not isinstance(scopes, list) or any(not isinstance(scope, str) for scope in scopes)
                        for alternative in security_requirements if isinstance(alternative, dict)
                        for name, scopes in alternative.items()):
                    fields['review_required'] = [f'malformed OpenAPI {security_scope} security requirements need review']
                components = obj.get('components', {})
                schemes = (components.get('securitySchemes', obj.get('securityDefinitions', {}))
                           if isinstance(components, dict) else None)
                if isinstance(schemes, dict):
                    fields['security_schemes'] = {name: _resolve(scheme, obj) for name, scheme in schemes.items()}
                else:
                    fields['review_required'] = ['malformed OpenAPI securitySchemes must be an object']
            schema = _resolve(media.get('schema',{}),obj)
            if schema: fields['request_schema'] = schema
            if 'example' in media: fields.update(body=media['example'],body_encoding='json' if 'json' in media_type else 'raw')
            elif media.get('examples'):
                example = _resolve(next(iter(media['examples'].values())),obj)
                if 'value' in example: fields.update(body=example['value'],body_encoding='json' if 'json' in media_type else 'raw')
            if '$ref' in request: fields['unresolved_request'] = request
            responses = operation.get('responses',{})
            success = sorted(int(code) for code in responses if re.fullmatch(r'2[0-9]{2}',str(code)))
            # Success and negative scenarios are separate; do not accept every declared error.
            fields['expected_statuses'] = success
            fields['declared_responses'] = responses
            contracts = {str(code):_resolve(response,obj) for code,response in responses.items() if str(code).isdigit() and int(code) in success}
            fields['response_contracts'] = contracts
            if any('$ref' in response for response in contracts.values()):
                fields['unresolved_response_contracts'] = contracts
            if success:
                response = contracts.get(str(success[0]),{})
                response_media = response.get('content',{}).get('application/json',{})
                if response_media.get('schema'):fields['response_schema'] = _resolve(response_media['schema'],obj)
            if operation.get('operationId'): fields['operation_id'] = operation['operationId']
            _append_endpoint(out,method,str(path),source,**fields)
    return out


def _parse_insomnia(obj, source):
    out = []
    for req in obj.get('resources',[]):
        if req.get('_type') != 'request':continue
        url = req.get('url','');headers = {h['name']:h.get('value','') for h in req.get('headers',[]) if h.get('name') and not h.get('disabled')}
        raw = req.get('body',{}).get('text')
        _append_endpoint(out,req.get('method','GET'),_url_path(url),source,raw_url=url,format='insomnia',headers=headers,**_body_fields(raw,headers))
    return out


def _parse_opencollection(obj, source):
    out = []
    for request in obj.get('requests',[]):
        url = request.get('path') or request.get('url')
        if not url: raise ValueError('OpenCollection request URL is missing')
        fields = {k:v for k,v in request.items() if k not in ('method','path','url','source','format')}
        _append_endpoint(out,request.get('method','GET'),_url_path(url),source,raw_url=request.get('url'),format='opencollection',**fields)
    return out


def _parse_wsdl(text, source):
    import io
    root = ET.fromstring(text)
    ns = {'wsdl':'http://schemas.xmlsoap.org/wsdl/','soap':'http://schemas.xmlsoap.org/wsdl/soap/','soap12':'http://schemas.xmlsoap.org/wsdl/soap12/'}
    namespaces = dict(value for _,value in ET.iterparse(io.StringIO(text),events=['start-ns']))
    bindings = root.findall('wsdl:binding',ns)
    by_name = {b.attrib.get('name'): b for b in bindings}
    if len(by_name) != len(bindings):raise ValueError('Ambiguous WSDL binding names')
    out = []
    for port in root.findall('.//wsdl:service/wsdl:port',ns):
        address = port.find('soap:address',ns)
        if address is None:address = port.find('soap12:address',ns)
        if address is None:continue
        reference = port.attrib.get('binding')
        if reference:
            prefix,sep,local = reference.partition(':')
            if not sep:local = prefix;prefix = ''
            namespace = namespaces.get(prefix)
            if namespace is not None and namespace != root.attrib.get('targetNamespace', namespace):
                raise ValueError('External WSDL bindings must be resolved explicitly')
            binding = by_name.get(local)
            if binding is None:raise ValueError('Unresolved WSDL port binding: '+reference)
        elif len(bindings)==1:
            binding=bindings[0]
        else:raise ValueError('WSDL port has no unambiguous binding')
        location=address.attrib['location']
        for operation in binding.findall('wsdl:operation',ns):
            action=operation.find('soap:operation',ns)
            if action is None:action=operation.find('soap12:operation',ns)
            extra={'raw_url':location,'format':'wsdl','operation':operation.attrib.get('name'),
                   'binding':binding.attrib.get('name'),'body_required':True,
                   'review_required':['SOAP envelope/schema must be supplied']}
            if action is not None:extra['soap_action']=action.attrib.get('soapAction','')
            _append_endpoint(out,'POST',_url_path(location),source,**extra)
    if not out:raise ValueError('WSDL has no resolved SOAP service operations; cannot invent an endpoint')
    return out


def _parse_bruno(text, source):
    method = re.search(r'^\s*(get|post|put|patch|delete|head|options)\s*\{',text,re.I|re.M)
    url = re.search(r'^\s*url:\s*(.+)$',text,re.M)
    if method is None or url is None:raise ValueError('Bruno HTTP method/URL is missing')
    raw_url = url.group(1).strip()
    headers = {}
    header_block = re.search(r'^headers\s*\{\s*\n(.*?)^\}',text,re.M|re.S)
    if header_block:
        for line in header_block.group(1).splitlines():
            key,sep,value = line.strip().partition(':')
            if sep:headers[key] = value.strip()
    body = re.search(r'^body:(json|text|xml)\s*\{\s*\n(.*?)^\}',text,re.M|re.S)
    fields = _body_fields(body.group(2).strip(),{**headers,'Content-Type':'application/json' if body.group(1)=='json' else headers.get('Content-Type','')}) if body else {}
    out = [];_append_endpoint(out,method.group(1),_url_path(raw_url),source,raw_url=raw_url,format='bruno',headers=headers,**fields)
    return out


def _load_structured(path, raw):
    if path.suffix.lower()=='.json':
        obj = json.loads(raw)
    elif path.suffix.lower() in ('.yaml','.yml'):
        if yaml is None:raise RuntimeError('PyYAML is required for YAML input; install it or supply JSON')
        obj = yaml.safe_load(raw)
    else:return None
    if not isinstance(obj,dict):raise ValueError('API document root must be an object')
    return obj


def parse_file(path, raw):
    ext = path.suffix.lower()
    if ext=='.wsdl' or (ext=='.xml' and 'definitions' in raw and 'wsdl' in raw.lower()):return _parse_wsdl(raw,str(path))
    if ext=='.bru':return _parse_bruno(raw,str(path))
    if ext in ('.curl','.sh','.txt'):return _parse_curl(raw,str(path))
    obj = _load_structured(path,raw)
    if obj is not None:
        if 'endpoints' in obj:
            endpoints=obj['endpoints']
            if not isinstance(endpoints,list) or not endpoints:
                raise ValueError('No endpoints in normalized contract')
            out=[]
            for endpoint in endpoints:
                if not isinstance(endpoint,dict) or not isinstance(endpoint.get('path'),str):
                    raise ValueError('Invalid normalized endpoint')
                extra={k:v for k,v in endpoint.items() if k not in {'method','path','source','format'}}
                if 'source' in endpoint:extra['declared_source']=endpoint['source']
                _append_endpoint(out,str(endpoint.get('method','')).upper(),_url_path(endpoint['path']),str(path),format='normalized',**extra)
            return out
        if 'openapi' in obj or 'swagger' in obj:return _parse_openapi(obj,str(path))
        if 'item' in obj:return _parse_postman(obj,str(path))
        if 'resources' in obj:return _parse_insomnia(obj,str(path))
        if 'requests' in obj:return _parse_opencollection(obj,str(path))
        raise ValueError('Unrecognized API document: '+str(path))
    return _parse_curl(raw,str(path))


def parse_zip(path):
    out = []
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            p = Path(member.filename)
            if member.is_dir() or p.suffix.lower() not in ('.json','.yaml','.yml','.wsdl','.xml','.bru','.curl','.sh','.txt'):continue
            out.extend(parse_file(p,archive.read(member).decode('utf-8')))
    return out


def parse_input(path):
    if path.is_dir():
        out = []
        for p in sorted(path.rglob('*')):
            if p.is_file() and p.suffix.lower() in ('.json','.yaml','.yml','.wsdl','.xml','.bru','.curl','.sh','.txt'):
                out.extend(parse_file(p,p.read_text(encoding='utf-8')))
        return out
    if path.suffix.lower()=='.zip':return parse_zip(path)
    return parse_file(path,path.read_text(encoding='utf-8'))


def dedupe(endpoints):
    seen, out = set(), []
    for endpoint in endpoints:
        # Payload/expectation variants are distinct scenarios, not duplicate paths.
        key = json.dumps(endpoint,sort_keys=True,ensure_ascii=False)
        if key not in seen:seen.add(key);out.append(endpoint)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    endpoints = dedupe(parse_input(args.input))
    if not endpoints:raise ValueError('No supported endpoints found; no inventory was generated')
    payload = {'input':str(args.input),'count':len(endpoints),'endpoints':endpoints}
    output = json.dumps(payload,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.write_text(output,encoding='utf-8');print(str(args.output))
    else:print(output,end='')

if __name__=='__main__':main()
