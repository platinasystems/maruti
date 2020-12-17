import time
import os
import re
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from platina_sdk import pcc_api as pcc
from aa.common import PccUtility as easy
from aa.common.Utils import banner, trace, pretty_print
from aa.common.Result import get_response_data, get_result
from aa.common.AaBase import AaBase
from aa.common.Cli import *

class Cli(AaBase):
    """ 
    Cli
    """

    def __init__(self):
        self.cmd = None
        self.host_ip = None
        self.nodes_ip=None
        self.linux_password = None
        self.linux_user = None
        self.pcc_username = None
        self.pcc_password = None
        self.remote_source = None
        self.local_destination = None
        self.platia_cli_version_cmd = None
        self.pcc_version_cmd = None
        self.backup_hostip = None
        self.restore_hostip = None
        self.backup_params = None
        self.backup_type = None
        super().__init__()

    ###########################################################################
    @keyword(name="CLI.Run")
    ###########################################################################
    def cli_run(self, *args, **kwargs):
        """
        CLI Run
        [Args]
            (str) cmd: 
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
        [Returns]
            (dict) Response: CLI Run response
        """
        self._load_kwargs(kwargs)
        banner("CLI.Run ip=%s [cmd=%s]" % (self.host_ip, self.cmd))
        return cli_run(self.host_ip, self.linux_user, self.linux_password, self.cmd)

    ###########################################################################
    @keyword(name="CLI.Truncate PCC Logs")
    ###########################################################################
    def cli_truncate_pcc_logs(self, *args, **kwargs):
        """
        CLI Truncate PCC Logs
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """
        self._load_kwargs(kwargs)
        print("kwargs"+str(kwargs))
        banner("CLI.Truncate PCC Logs ip=%s" % self.host_ip)
        ret = cli_truncate_pcc_logs(self.host_ip, self.linux_user, self.linux_password)
        print("Response"+str(ret))
        if ret.stderr == "":
            return "OK"
        else:
            return ret.stderr


    ###########################################################################
    @keyword(name="CLI.Copy PCC Logs")
    ###########################################################################
    def cli_copy_pcc_logs(self, *args, **kwargs):
        """
        CLI Copy+ PCC Logs
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
            (str) remote_source
            (str) local_destination

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Copy PCC Logs ip=%s" % self.host_ip)
        return cli_copy_pcc_logs(self.host_ip, self.linux_user, self.linux_password)

    ###########################################################################
    @keyword(name="CLI.Pcc Down")
    ###########################################################################
    def cli_pcc_down(self, *args, **kwargs):
        """
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Pcc Down ip=%s" % self.host_ip)
        cmd="sudo /home/pcc/platina-cli-ws/platina-cli down -p {}".format(self.pcc_password)
        print("Making PCC Down ...")
        trace("Making PCC Down ...")
        print("Command:"+str(cmd))
        output=cli_run(self.host_ip, self.linux_user, self.linux_password, cmd)
        print("Output:"+str(output))
        trace("Output:"+str(output))
        if re.search("FAIL",str(output)):
            return "Error"
        else:
            return "OK"

    ###########################################################################
    @keyword(name="CLI.Pcc Cleanup")
    ###########################################################################
    def cli_pcc_cleanup(self, *args, **kwargs):
        """
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
            
        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """      
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Pcc Cleanup ip=%s" % self.host_ip)
        
        volume_cmd="printf 'y\n' |sudo docker volume prune"
        system_cmd="printf 'y\n'|sudo docker system prune"
        network_cmd="printf 'y\n'|sudo docker network prune"
        container_cmd="printf 'y\n'|sudo docker container prune"
        image_cmd="sudo docker rmi -f `docker images -q`"
        
        print("Volume Is Pruning .....")
        print("Command:"+str(volume_cmd))
        trace("Volume Is Pruning .....")
        volume_output=cli_run(self.host_ip, self.linux_user, self.linux_password, volume_cmd)
        trace(str(volume_output))
        print("System Is Pruning .....")
        print("Command:"+str(system_cmd))
        trace("System Is Pruning .....")
        system_output=cli_run(self.host_ip, self.linux_user, self.linux_password, system_cmd)
        trace(str(system_output))
        print("Network Is Pruning .....")
        print("Command:"+str(network_cmd))
        trace("Network Is Pruning .....")        
        network_output=cli_run(self.host_ip, self.linux_user, self.linux_password, network_cmd)
        trace(str(network_output))
        print("Container Is Pruning .....")
        print("Command:"+str(container_cmd))
        trace("container Is Pruning .....")        
        container_output=cli_run(self.host_ip, self.linux_user, self.linux_password, container_cmd)
        trace(str(container_output))
        print("Removing Docker Images .....")
        print("Command:"+str(image_cmd))
        trace("Removing Docker Images .....")
        image_output=cli_run(self.host_ip, self.linux_user, self.linux_password, image_cmd) 
        trace(str(image_output))
        
        return "OK"
 
    ###########################################################################
    @keyword(name="CLI.Pcc Platina Cli Version")
    ###########################################################################
    def cli_pcc_platina_cli_version(self, *args, **kwargs):
        """
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
            (str) platia_cli_version_cmd:

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """   
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Pcc Platina Cli Version ip=%s" % self.host_ip)
        remove_cmd="sudo rm -rf /home/pcc/platina-cli-ws; sudo rm -rf /home/pcc/platina-cli.tar.gz"
        unzip_cmd="sudo tar -xvf platina-cli.tar.gz"
        if self.platia_cli_version_cmd:
            print("Removing existing platina cli ...")
            trace("Removing existing platina cli ...")
            print("Command:"+str(remove_cmd))
            remove_output=cli_run(self.host_ip, self.linux_user, self.linux_password, remove_cmd)
            trace(str(remove_output))
            print("Installing new platina cli ...")
            trace("Installing new platina cli ...")
            print("Command:"+str(self.platia_cli_version_cmd))
            cmd_output=cli_run(self.host_ip, self.linux_user, self.linux_password, self.platia_cli_version_cmd)
            trace(str(cmd_output))
            print("Unzipping new platina cli ...")
            trace("Unzipping new platina cli ...")
            print("Command:"+str(unzip_cmd))            
            unzip_output=cli_run(self.host_ip, self.linux_user, self.linux_password, unzip_cmd)
            trace(str(unzip_output))

        return "OK"       
 
    ###########################################################################
    @keyword(name="CLI.PCC Pull Code")
    ###########################################################################
    def cli_pull_code(self, *args, **kwargs):
        """
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
            (str) pcc_version_cmd:

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """     
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.PCC Pull Code ip=%s" % self.host_ip)
        if self.pcc_version_cmd:
            print("Pulling the code ....")
            trace("Pulling the code ....")
            print("Command:"+str(self.pcc_version_cmd))
            pull_output=cli_run(self.host_ip, self.linux_user, self.linux_password, self.pcc_version_cmd)
            print("Output:"+str(pull_output))
            trace("Output:"+str(pull_output))
            if re.search("FAIL",str(pull_output)):
                 print(str(pull_output))
                 return "Error"
            else:
                return "OK"
        else:
            print("Pull/pcc_version_cmd command is empty !!")
            return "OK"
        
    ###########################################################################
    @keyword(name="CLI.Pcc Set Keys")
    ###########################################################################
    def cli_pcc_set_keys(self, *args, **kwargs):
        """
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
            (list) nodes_ip:

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """      
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Pcc Set Keys ip=%s" % self.host_ip)
        flag=[]
        if not self.nodes_ip:
            print("Nodes Ips are missing, Please provide ...")
            return "Error"
        for node_ip in eval(str(self.nodes_ip)):
            print("Setting keys for {} ...".format(str(node_ip)))
            trace("Setting keys for {} ...".format(str(node_ip)))
            cmd="sudo docker exec platina-executor sh -c 'ssh -o StrictHostKeyChecking=no -i /root/.ssh/id_rsa_ansible pcc@{} -t echo -e 'yes''".format(node_ip)
            print("Command: "+str(cmd))
            cmd_output=cli_run(self.host_ip, self.linux_user, self.linux_password, cmd)
            trace(cmd_output)
            if re.search("failed",str(cmd_output)):
                 flag.append(node_ip)
            else:
                continue
        if flag:
            print("failed while copying the keys for {}".format(flag))
            return "Error"   
        return "OK"


    ###########################################################################
    @keyword(name="CLI.Pcc Add Iscsi Drives")
    ###########################################################################
    def cli_pcc_add_iscsi_drives(self, *args, **kwargs):
        """
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Pcc Add Iscsi Drives")
        cmd="sudo ansible-playbook -i ./pcc-inventory ./site.yml"
        print("Command:"+str(cmd))
        output=cli_run(self.host_ip, self.linux_user, self.linux_password, cmd)
        print("Output:"+str(output))
        trace("Output:"+str(output))
        if re.search("no tasks failed",str(output)):
            return "OK"
        else:
            return "Error"
            
    ###########################################################################
    @keyword(name="CLI.Backup PCC Instance")
    ###########################################################################
    def backup_pcc_instance(self,*args,**kwargs):
        banner("CLI.Backup PCC Instance")
        self._load_kwargs(kwargs)
        trace("Kwargs are: " + str(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        if (self.backup_type == "local") and (self.backup_params == "all"):
            cmd = "sudo /home/pcc/platina-cli-ws/platina-cli backup -p {}".format(self.pcc_password)

        if (self.backup_type == "local") and (self.backup_params != "all"):
            cmd = "sudo /home/pcc/platina-cli-ws/platina-cli backup -p {} -t {}".format(self.pcc_password, self.backup_params)

        if (self.backup_type == "remote"):
            cmd = "sudo /home/pcc/platina-cli-ws/platina-cli backup -p {} --url http://{}:9001 --id minio --secret minio123".format(self.pcc_password, self.backup_hostip)

        trace("Command: " + str(cmd) + " is getting executed")
        cmd_op=cli_run(self.host_ip,self.linux_user,self.linux_password,cmd)
        print("cmd op: {}".format(str(cmd_op)))
        if re.search("FAIL",str(cmd_op)):
            print("Failed to backup, result is: \n {}".format(str(cmd_op)))
            return "Error: Failed to backup"
        else:
            cmd_file="sudo test -f /home/pcc/platina-cli-ws/master.gpg && echo 'True'"
            cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,cmd_file)
            print("Checking if keys folder exist or not:"+str(cmd_out))
            if re.search("True",str(cmd_out)):
                if self.backup_type=="local":
                    cmd_local_file="sudo test -d /home/pcc/platina-cli-ws/keys/local && echo 'True' || echo 'False'"
                    cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,cmd_local_file)
                    print("Checking if keys folder exist or not:"+str(cmd_out))
                    if re.search("False",str(cmd_out)):
                        folder_cmd="sudo mkdir -p /home/pcc/platina-cli-ws/keys/local"
                        cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,folder_cmd)
                        print("Folder check:"+str(cmd_out))
                        move_cmd="sudo mv /home/pcc/platina-cli-ws/*.gpg /home/pcc/platina-cli-ws/keys/local/."
                        cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,move_cmd)
                        print("Key moving:"+str(cmd_out))
                    else:
                        move_cmd="sudo mv /home/pcc/platina-cli-ws/*.gpg /home/pcc/platina-cli-ws/keys/local/."
                        cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,move_cmd)
                        print("Key moving:"+str(cmd_out))
                elif self.backup_type=="remote":
                    cmd="sudo test -d /home/pcc/platina-cli-ws/keys/remote && echo 'True' || echo 'False'"
                    cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,cmd)
                    print("Checking if keys folder exist or not:"+str(cmd_out))
                    if re.search("False",str(cmd_out)):
                        folder_cmd="sudo mkdir -p /home/pcc/platina-cli-ws/keys/local"
                        cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,folder_cmd)
                        move_cmd="sudo mv /home/pcc/platina-cli-ws/*.gpg /home/pcc/platina-cli-ws/keys/remote/."
                        print("Folder check:"+str(cmd_out))
                        cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,move_cmd)
                        print("Key moving:"+str(cmd_out))
                    else:
                        move_cmd="sudo mv /home/pcc/platina-cli-ws/*.gpg /home/pcc/platina-cli-ws/keys/remote/."
                        cmd_out=cli_run(self.host_ip,self.linux_user,self.linux_password,move_cmd)
                        print("Key moving:"+str(cmd_out))
            return "OK"

    ###########################################################################
    @keyword(name="CLI.Restore PCC Instance")
    ###########################################################################
    def restore_pcc_instance(self,*args,**kwargs):
        banner("CLI.Restore PCC Instance")
        self._load_kwargs(kwargs)
        trace("Kwargs are: " + str(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        
        if (self.backup_type == "remote"):
            cmd="sudo /home/pcc/platina-cli-ws/platina-cli restore -p {} -t {} --url http://{}:9001 --id minio --secret minio123 --privateKey /home/pcc/platina-cli-ws/keys/remote/master.gpg".format(self.pcc_password, self.backup_params, self.restore_hostip)
            
        if (self.backup_type == "local") and (self.backup_params == "all"):
            cmd = "sudo /home/pcc/platina-cli-ws/platina-cli restore -p {} --privateKey /home/pcc/platina-cli-ws/keys/local/master.gpg".format(self.pcc_password)
        
        if (self.backup_type == "local") and (self.backup_params != "all"):
            cmd = "sudo /home/pcc/platina-cli-ws/platina-cli backup -p {} -t {} --privateKey /home/pcc/platina-cli-ws/keys/local/master.gpg".format(self.pcc_password, self.backup_params)
        
        trace("Command" + str(cmd) + "is getting executed")
        cmd_op=cli_run(self.host_ip,self.linux_user,self.linux_password,cmd)
        print("cmd op: {}".format(str(cmd_op)))
        if re.search("FAIL",str(cmd_op)):
            print("Failed to backup, result is: \n {}".format(str(cmd_op)))
            return "Error: Failed to backup"
        else:
            return "OK"
            
    ###########################################################################
    @keyword(name="CLI.Reboot Node")
    ###########################################################################
    def reboot_node(self,*args,**kwargs):
        banner("CLI.Reboot Node")
        self._load_kwargs(kwargs)
        trace("Kwargs are: " + str(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        cmd="sudo reboot -f"
        trace("Command" + str(cmd) + "is getting executed")
        cmd_op=cli_run(self.host_ip,self.linux_user,self.linux_password,cmd)
        print("cmd op: {}".format(str(cmd_op)))
        trace("Reboot undergoing - Sleeping for 5 minutes")
        time.sleep(5*60) # Sleeping 5 mins
        trace("Done sleeping")
        return "OK"
