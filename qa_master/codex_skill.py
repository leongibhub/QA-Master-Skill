"""Install a self-contained Codex skill; no model or business-system calls."""
from __future__ import annotations

import hashlib
import json
import os
import stat
from importlib import resources
from pathlib import Path
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
from uuid import uuid4

MANIFEST = '.qa-master-install.json'


class SkillInstallError(ValueError):
    pass


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _linked(path):
    """Reject symlinks and Windows junction/reparse points without following them."""
    return path.is_symlink() or bool(
        getattr(path.lstat(), 'st_file_attributes', 0)
        & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)
    )


def _files(root, prefix=''):
    for item in sorted(root.iterdir(), key=lambda value: value.name):
        name = prefix + item.name
        if item.is_dir():
            yield from _files(item, name + '/')
        elif item.is_file() and item.name.endswith(('.md', '.py', '.json')):
            yield name, item.read_bytes()


def skill_bundle():
    """Use package resources, including when installed from a fresh wheel."""
    package = resources.files('qa_master')
    result = dict(_files(package.joinpath('skills', 'codex')))
    if 'SKILL.md' not in result:
        raise SkillInstallError('SKILL_RESOURCE_MISSING')
    for item in package.iterdir():
        if item.is_file() and item.name.endswith('.py'):
            result['scripts/qa_master/' + item.name] = item.read_bytes()
    for name, data in _files(package.joinpath('skills', 'professional')):
        result['scripts/qa_master/skills/professional/' + name] = data
    result['scripts/qa.py'] = (
        'from pathlib import Path\n'
        'import sys\n'
        'sys.path.insert(0, str(Path(__file__).resolve().parent))\n'
        'from qa_master.__main__ import main\n'
        'if __name__ == "__main__":\n'
        '    raise SystemExit(main())\n'
    ).encode('utf-8')
    return result


def default_target(*, user=False, project=None):
    base = Path.home() if user else Path(project or Path.cwd())
    return base / '.agents' / 'skills' / 'qa-master'


def _existing(target):
    if _linked(target) or not target.is_dir():
        raise SkillInstallError('SKILL_TARGET_CONFLICT')
    try:
        manifest_path = target / MANIFEST
        if _linked(manifest_path):
            raise ValueError()
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if (not isinstance(manifest, dict) or set(manifest) != {'schema_version', 'files'}
                or type(manifest['schema_version']) is not int or manifest['schema_version'] != 1
                or not isinstance(manifest['files'], dict) or not manifest['files']):
            raise ValueError()
        found = {}
        for item in target.rglob('*'):
            if _linked(item):
                raise ValueError()
            if item.is_file():
                name = item.relative_to(target).as_posix()
                if item.parent.name == '__pycache__' and item.suffix == '.pyc':
                    continue
                if name != MANIFEST:
                    found[name] = _digest(item.read_bytes())
        if found != manifest['files']:
            raise ValueError()
    except (OSError, ValueError, TypeError, KeyError):
        raise SkillInstallError('SKILL_TARGET_MODIFIED') from None
    return found


def install_skill(target=None, *, user=False, project=None, update=False):
    target = Path(target) if target is not None else default_target(user=user, project=project)
    if (target.exists() or target.is_symlink()) and _linked(target):
        raise SkillInstallError('SKILL_TARGET_CONFLICT')
    target = target.absolute()
    bundle = skill_bundle()
    hashes = {name: _digest(data) for name, data in sorted(bundle.items())}
    previous = None
    if target.exists():
        previous = _existing(target)
        if previous == hashes:
            return {'status': 'UNCHANGED', 'target': str(target), 'files': len(hashes)}
        if not update:
            raise SkillInstallError('SKILL_UPDATE_REQUIRED')
    target.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    recovery = None
    with tempfile.TemporaryDirectory(prefix='.qa-master-stage-', dir=target.parent) as temporary:
        staged = Path(temporary) / 'qa-master'
        staged.mkdir()
        for name, data in bundle.items():
            output = staged / name
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
        (staged / MANIFEST).write_text(json.dumps({'schema_version': 1, 'files': hashes},
                                                 sort_keys=True, indent=2) + '\n', encoding='utf-8')
        if target.exists():
            if _existing(target) != previous:
                raise SkillInstallError('SKILL_TARGET_MODIFIED')
            identifier = uuid4().hex
            backup = target.with_name('qa-master.backup-' + identifier + '.zip')
            # Keep the actual previous tree outside TemporaryDirectory. Open writers
            # can still change it; an archive alone cannot preserve those late edits.
            # Standard Codex installs must not discover the retained old SKILL.md.
            recovery_base = target.parent.parent if target.parent.name == 'skills' else target.parent
            recovery_root = recovery_base / '.qa-master-recovery'
            if recovery_root.exists() and _linked(recovery_root):
                raise SkillInstallError('SKILL_TARGET_CONFLICT')
            recovery_root.mkdir(exist_ok=True)
            recovery = recovery_root / ('qa-master.previous-' + identifier)
            os.rename(target, recovery)
        try:
            if recovery is not None:
                if _existing(recovery) != previous:
                    raise SkillInstallError('SKILL_TARGET_MODIFIED')
                with ZipFile(backup, 'x', compression=ZIP_DEFLATED) as archive:
                    for item in sorted(recovery.rglob('*')):
                        if _linked(item):
                            raise SkillInstallError('SKILL_TARGET_MODIFIED')
                        if item.is_file():
                            archive.writestr(item.relative_to(recovery).as_posix(), item.read_bytes())
                if _existing(recovery) != previous:
                    raise SkillInstallError('SKILL_TARGET_MODIFIED')
            os.rename(staged, target)
        except (OSError, SkillInstallError):
            if recovery is not None and not target.exists():
                try:
                    os.rename(recovery, target)
                except OSError:
                    raise SkillInstallError('SKILL_INSTALL_RECOVERY_REQUIRED:' + str(recovery)) from None
            raise
    return {'status': 'UPDATED' if backup else 'INSTALLED', 'target': str(target),
            'files': len(hashes), 'backup': str(backup) if backup else None,
            'recovery_directory': str(recovery) if recovery else None,
            'execution': 'NOT_EXECUTED'}
