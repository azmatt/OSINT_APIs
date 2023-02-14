import boto3
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', type=str, required=True, help='Source Image (one face only)')
parser.add_argument('-t', type=str, required=True, help='Target Image')
args = parser.parse_args()
source_image = args.s
target_image = args.t

client=boto3.client('rekognition')

imageSource=open('./{}'.format(source_image),'rb')
imageTarget=open('./{}'.format(target_image),'rb')
response=client.compare_faces(SimilarityThreshold=0,
                              SourceImage={'Bytes': imageSource.read()},
                              TargetImage={'Bytes': imageTarget.read()})
#print(response)  ### Detailed Information

for faceMatch in response['FaceMatches']:
    position = faceMatch['Face']['BoundingBox']
    similarity = str(faceMatch['Similarity'])
    print('[+] The face at ' +
           str(position['Left']) + ' ' +
           str(position['Top']) +
           ' matches with ' + similarity + '% confidence')

imageSource.close()
imageTarget.close()               
