exports.config={runner:'local',specs:['./checkout.spec.cjs'],maxInstances:2,capabilities:[{browserName:'chrome'}],framework:'mocha',reporters:['spec'],mochaOpts:{timeout:10000},logLevel:'warn'};
