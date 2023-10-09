import React, { useState } from 'react';
import { S3 } from 'aws-sdk';

const AwsSecrets = {
  region: process.env.REACT_APP_AWS_REGION,
  accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
};

const InputS3Secrets = {
  Bucket: process.env.REACT_APP_S3_INPUT_BUCKET_NAME as string,
  Key: process.env.REACT_APP_S3_INPUT_OBJECT_KEY as string,
};

const OutputS3Secrets = {
  Bucket: process.env.REACT_APP_S3_OUTPUT_BUCKET_NAME as string,
  Key: process.env.REACT_APP_S3_OUTPUT_OBJECT_KEY as string,
};

const s3 = new S3(AwsSecrets);

const S3Editor: React.FC = () => {
  const [content, setContent] = useState<string>('');

  const loadContent = async () => {
    const data = await s3.getObject(InputS3Secrets).promise();
    setContent(data.Body?.toString() || '');
  };

  const saveContent = async () => {
    await s3.putObject({ ...OutputS3Secrets, Body: content }).promise();
  };

  return (
    <div>
      <label htmlFor="content">Content:</label>
      <textarea id="content" value={content} onChange={e => setContent(e.target.value)} placeholder="Enter content here" aria-label="Content" />
      <button type="button" onClick={loadContent} aria-label="Load">Load</button>
      <button type="button" onClick={saveContent} aria-label="Save">Save</button>
    </div>
  );
};

export default S3Editor;
