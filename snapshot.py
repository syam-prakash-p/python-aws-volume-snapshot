import boto3
from datetime import datetime
volume_id_list = ["vol-0ef633e7877f18763"]  # <-- add volumes to the list (snapshot required volumes)


def collect_previous_snapshot_data(data):
     """
     collect current snapshot details
     
     """
    previous_snapshot_dict = {}
    for item in data['Snapshots']:
        if item['VolumeId'] in volume_id_list:
            previous_snapshot_dict[item['VolumeId']] = item['SnapshotId']
    return previous_snapshot_dict


client = boto3.client('ec2')
data = client.describe_snapshots()
snapshot_dict = collect_previous_snapshot_data(data)

####### create snapshots #########
for volume_id in volume_id_list:
    response = client.create_snapshot(
        Description=f"snapshot of {volume_id} - {datetime.utcnow()}",
        VolumeId=volume_id,
        DryRun=False)
    print(f"snapshot creation started : volume id:{response['VolumeId']} ---> snapshot id: {response['SnapshotId']}")
    if snapshot_dict.get(volume_id):
        del_response = client.delete_snapshot(
            SnapshotId=snapshot_dict.get(volume_id),
            DryRun=False
        )
        print(f"deleting previous snapthost of volume: {volume_id} ----> snapshot id {snapshot_dict.get(volume_id)}")




