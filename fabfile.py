from fabric.api import run
from fabric.api import env
import boto.ec2
import time
from fabric.api import prompt
from fabric.api import execute
from fabric.api import sudo
from fabric.contrib.project import rsync_project
from fabric.contrib.project import upload_project

env.hosts = ['localhost', ]
env.aws_region = 'us-west-2'

USER = 'ubuntu'
KEY_FILE = '~/.ssh/seattle_emergency.pem'

# Bookapp CONSTANTS
HOST = 'ec2-52-10-45-174.us-west-2.compute.amazonaws.com'
LOCAL_PROJECT_DIR = '~/projects/seattle/project/'
REMOTE_PROJECT_DIR = '/home/ubuntu/seattle_emergency'
NGINX_CONFIG = '~/projects/seattle/nginx_config/simple_nginx_config'


def host_type():
    run('uname -s')


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=False, timeout=60, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'seattle_emergency.pem'
    security_group = 'ssh-access'
    image_id = 'ami-b5471c85'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [i for i in reservations.instances if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if choice not in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    env.active_instance
    execute(command, hosts=selected_hosts)


def stop_instance():
    select_instance()
    conn = get_ec2_connection()
    conn.stop_instances(instance_ids=env.active_instance.id)


def terminate_instance():
    select_instance(state='stopped')
    conn = get_ec2_connection()
    conn.terminate_instances(instance_ids=env.active_instance.id)


def run_command_on_given_server(command, host):
    given_host = ['ubuntu@' + host]
    execute(command, hosts=given_host)


def _install_nginx():
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')


def _config_nginx():
    upload_project(NGINX_CONFIG)
    sudo('mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.orig')
    sudo('mv simple_nginx_config /etc/nginx/sites-available/default')
    sudo('/etc/init.d/nginx restart')


def _intialize_instance():
    provision_instance()


def _deploy():
    rsync_project(local_dir=LOCAL_PROJECT_DIR,
                  remote_dir=REMOTE_PROJECT_DIR,
                  exclude='*.pyc')
    sudo('/usr/bin/supervisorctl restart bookapp')


def _install_supervisor():
    sudo('apt-get install supervisor')


def install_nginx():
    '''Install NGINX'''
    run_command_on_selected_server(_install_nginx)


# Create instance and set it up from scratch

def total_setup():
    provision_instance(wait_for_running=1)
    setup()

# Setup instance for app


def setup():
    ''' Setup an existing instance.'''
    select_instance()
    selected_hosts = env.active_instance.public_dns_name
    env.active_instance
    selected_hosts
    run_command_on_given_server(_install_nginx, selected_hosts)
    run_command_on_given_server(_install_supervisor, selected_hosts)


# Seattle Project
# Deployment functions for Bookapp


def deploy():
    '''Push app to AWS'''
    run_command_on_given_server(_deploy, HOST)


def cnginx():
    '''Configure NGINX'''
    run_command_on_given_server(_config_nginx, HOST)
