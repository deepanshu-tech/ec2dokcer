from logging import exception
import boto3
import ec2_services as ec
# Creating the connection with the resource of AWS EC2 service
from flask import *
app=Flask(__name__)

print("working")
@app.route('/')
def home():
    # return "Hello EC2 "
    return render_template('index.html')



@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/create_ec2',methods=['POST'])
def create_ec2():
    ec2 = boto3.client('ec2')
    if request.method=='POST':
        image_id=request.form['imageid']
        mincount=int(request.form['mincount'])
        maxcount=int(request.form['maxcount'])
        instancetype=request.form['instancetype']
        try:

            instances = ec2.run_instances(
                ImageId=image_id,
                MinCount=mincount, #MinCount: Minimum number of EC2 instances to create
                MaxCount=maxcount, #MaxCount: Maximum number of EC2 instances to create
                InstanceType=instancetype,)
            return render_template('success.html')
        except exception as e:
            print("Sorry!", e.__class__, "occurred.")
     
    
    # print("EC2 Instance Launched succesfully")

@app.route('/show')
def show():
    ec2 = boto3.client('ec2')
    # try:
    print("logging done")
    response = ec2.describe_instances().get('Reservations')
    return render_template('show.html',response=response)
    # except exception as e:
        # print("Sorry!", e.__class__, "occurred.")

@app.route('/start/<id>')
def start(id):
    ec2=boto3.client('ec2')
    try:
        response = ec2.start_instances(InstanceIds=[id])   
        return redirect(url_for('show'))
    except exception as e:
        print("Sorry!", e.__class__, "occurred.")
        

@app.route('/stop/<id>')
def stop_instance(id):
    # instance_id=int(instance_id)
    ec2 = boto3.client("ec2")
    try:
        response = ec2.stop_instances(InstanceIds=[id])
        return redirect(url_for('show'))
    except exception as e:
        print("Sorry!", e.__class__, "occurred.")
    

@app.route('/terminate/<id>')
def terminate_instance(id):
    ec2 = boto3.client("ec2")
    try:
        response = ec2.terminate_instances(InstanceIds=[id])
        return redirect(url_for('show'))
    except exception as e:
        print("Sorry!", e.__class__, "occurred.")
    

# def show_ec2_instances():
#     instances = ec2.instances.all()
#     for i in instances:
#         print(i.id)
#     # print(instances["Instances"][0]["InstanceId"])


# def get_public_ip(instance_id):
#     ec2_client = boto3.client("ec2")
#     reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

#     for reservation in reservations:
#         for instance in reservation['Instances']:
#             print(instance.get("PublicIpAddress"))


# get_public_ip('i-048b8cf7815d335ce')

# def get_running_instances():
#     ec2_client = boto3.client("ec2")
#     reservations = ec2_client.describe_instances(Filters=[
#         {
#             # "Name": "instance-state-name",
#             "Values": ["running"]
#         }
#     ]).get("Reservations")
#     for reservation in reservations:
#         for instance in reservation["Instances"]:
#             instance_id = instance["InstanceId"]
#             instance_type = instance["InstanceType"]
#             public_ip = instance["PublicIpAddress"]
#             private_ip = instance["PrivateIpAddress"]
#             time=instance['LaunchTime']
#             print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip} ,{time}")
# get_running_instances()







# @app.route('/del/<id>')
# def delete(id):
#     return "delete called %s" %id

# @app.route('stop')
# @app.route('/show')
# def show():
#     ec2 = boto3.client('ec2')
#     response = ec2.describe_instances().get('Reservations')
        # data=[]
#     for reservation in response:
#         for instance in reservation["Instances"]:
#             instance_id = instance["InstanceId"]
#             instance_type = instance["InstanceType"]
#             # public_ip = instance["PrivateIpAddress"]
#             # private_ip = instance["PrivateIpAddress"]
#             #will show error to ip becouse terminated instance do not have ip
#             state=instance['State']['Name']
#             time=instance['LaunchTime']
#             # print(f"{instance_id},{instance_type},{state},{time}")
            
#     return render_template('show.html',data=[instance_id,instance_type,state,time])



if __name__=='__main__':
    app.run(debug=True,port=5001,host='0.0.0.0')
