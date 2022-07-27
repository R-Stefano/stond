const {Storage} = require('@google-cloud/storage');
const storage = new Storage();
const configs = require('../configs');
const GCBucket = storage.bucket(configs.cloud.bucket_name);
const { v1: uuidv1 } = require('uuid');
const path = require('path')
const os = require('os')
const fs = require('fs');

exports.save = async (fileBase64, fileType, destPath = null) => {
    /**
     * Upload the file and return filename
     */
    const filename = uuidv1()
    const localFilePath  = path.join(os.tmpdir(), filename);
    const buffer = Buffer.from(fileBase64, 'base64');
    fs.writeFileSync(localFilePath, buffer);

    if (fileType.includes(".")) {
        fileType = fileType.replace(".", "")
    }
    
    let destFilePath = `${filename}.${fileType}`
    if (destPath) {
        destFilePath = `${destPath}/${filename}.${fileType}`
    }

    destFilePath =`resources/${destFilePath}`

    await GCBucket.upload(localFilePath, { destination: destFilePath})

    return `${filename}.${fileType}`
}
