import os
import sys
import shutil
import re

from cloudinit.settings import PER_INSTANCE
from cloudinit import util


frequency = PER_INSTANCE

def replace_config(goagent_file, goagent_key, goagent_value):
  found_key = False
  outputfile = open(goagent_file + ".tmp","w")
  if os.path.exists(goagent_file):
    inputfile = open(goagent_file,"r")
    for line in inputfile.readlines():
      if re.match('^'+goagent_key+'[\s]*=',line):
        found_key = True
        outputfile.write("%s=%s\n" % (goagent_key,goagent_value))
      else:
        outputfile.write(line)
  if not found_key:
    outputfile.write("%s=%s\n" % (goagent_key,goagent_value))
  outputfile.close()
  if os.path.exists(goagent_file):
    inputfile.close()
  shutil.move(goagent_file + ".tmp", goagent_file)


def handle(name, cfg, cloud, log, _args):
  try:

    # Go Agent Config Prefix
    go_agent_prefix = "goagent_"
    go_agent_default = "/etc/default/go-agent"
    
    go_server_prefix = "goserver_"
    go_server_config_dir = "/var/lib/go-agent/config"
    if not os.path.exists(go_server_config_dir):
      os.makedirs(go_server_config_dir)
      util.chownbyname(go_server_config_dir,"go","go")
    go_server_config = go_server_config_dir + "/autoregister.properties"

    # Make sure Go Agent is not running
    util.subp(['service', 'go-agent', 'stop'])

    md = cloud.datasource.metadata
    for key in md['meta']:
      if key.startswith(go_agent_prefix):
        replace_config(go_agent_default,key[len(go_agent_prefix):],md['meta'][key])
      elif key.startswith(go_server_prefix):
        replace_config(go_server_config,key[len(go_server_prefix):],md['meta'][key])

    # Use Openstack Instance ID as Go Elastic Agent ID for auto registraton
    replace_config(go_server_config,"agent.auto.register.elasticAgent.agentId",md['uuid'])
    
    if os.path.exists(go_server_config):
      util.chownbyname(go_server_config,"go","go")

    if os.path.exists(go_agent_default):
      util.chmod(go_agent_default,0644)
    
    # Start Go Agent
    util.subp(['service', 'go-agent', 'start'])

  except:
    log.debug("Error configuring Go Agent")
    return
