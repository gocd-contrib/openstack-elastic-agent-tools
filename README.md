# openstack-elastic-agent-tools
Files that can be used to create openstack image to configure and speed up job that use elastic agent

## Image configuration

1. cloudinit module `cc_openstack_gocd.py` should be placed in `<PYTHON_ROOT>/dist-packages/cloudinit/config/cc_openstack_gocd.py`,
for example for python3 on debian systems that would be `/usr/lib/python3/dist-packages/cloudinit/config/cc_openstack_gocd.py`.
2. Then module must be enabled in `/etc/cloud/cloud.cfg` under cloud_final_modules like so:
```yaml
# The modules that run in the 'final' stage
cloud_final_modules:
 - openstack_gocd
 - package-update-upgrade-install
# ...
```

### Debugging

You can rerun final stage of cloud-init:

1. Remove
```
/var/lib/cloud/instance/boot-finished or /var/lib/cloud/instances/$UUID/boot-finished
/var/lib/cloud/instances/$UUID/sem/
```
2. Run `cloud-init modules --mode final`

You can check that `openstack_gocd` module was executed:
```
cat /var/log/cloud-init.log | grep cc_openstack_gocd
May 19 09:22:31 goea-anjarf86vicg [CLOUDINIT] stages.py[DEBUG]: Running module openstack_gocd (<module 'cloudinit.config.cc_openstack_gocd' from '/usr/lib/python3/dist-packages/cloudinit/config/cc_openstack_gocd.py'>) with frequency once-per-instance
```
