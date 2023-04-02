const express = require('express');
const cors = require('cors');
//const fs = require('fs');
const xlsx = require('xlsx');
const multer = require('multer');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');
// const readline = require('readline');
// const rl = readline.createInterface({
//   input: process.stdin,
//   output: process.stdout
// });
// let {PythonShell} =require('python-shell');

const app = express();
const port = 3100;

app.use(cors({
    origin: 'http://localhost:3000',
    optionsSuccessStatus: 200
}));
app.use(bodyParser.json({ limit: '50mb' }));
app.use(express.json());
app.use(express.static('public'));

let worksheet1 = xlsx.utils.aoa_to_sheet([
    ['', ''],
    ['', 0],
    ['', 0],
  ]);
let worksheet2 = xlsx.utils.aoa_to_sheet([
    ['', ''],
    ['', 0],
    ['', 0],
  ]);
let worksheet3 = xlsx.utils.aoa_to_sheet([
    ['', ''],
    ['', 0],
    ['', 0],
  ]);

// Create a multer storage object
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

// Create a multer upload object
const upload = multer({ storage: storage }).array('files');

app.post('/upload', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to upload files' });
    }

    // Get the files from the request
    const files = req.files;
    const area = req.body.area;
    const diesel = req.body.diesel;
    const district = req.body.district;

    // Read the first file
    const workbook1 = xlsx.readFile(files[0].path);
    worksheet1 = workbook1.Sheets[workbook1.SheetNames[0]];
    const data1 = xlsx.utils.sheet_to_json(worksheet1, { header: 1 });
    // console.log('Data from file 1:', data1);

    // Read the second file
    const workbook2 = xlsx.readFile(files[1].path);
    worksheet2 = workbook2.Sheets[workbook2.SheetNames[0]];
    const data2 = xlsx.utils.sheet_to_json(worksheet2, { header: 1 });
    // console.log('Data from file 2:', data2);

    // Read the third file
    const workbook3 = xlsx.readFile(files[2].path);
    worksheet3 = workbook3.Sheets[workbook3.SheetNames[0]];
    const data3 = xlsx.utils.sheet_to_json(worksheet3, { header: 1 });
    // console.log('Data from file 3:', data3);

    // Get the file paths separately
    const file1path = files[0].path;
    const file2path = files[1].path;
    const file3Path = files[2].path;

    console.log('File path 1:', file1path);
    console.log('File path 2:', file2path);
    console.log('File path 3:', file3Path);

    console.log('Area:', area);
    console.log('Diesel:', diesel);
    console.log('District:', district);

     // Spawn the Python script with the file paths
    // const pythonScript = spawn('python', ["C:/FYP/myNode/test.py", file1Path, file2Path,district,area,diesel]);
    
    const pythonScriptPath = path.join(__dirname,'test.py');
    const args = [file1path, file2path, district, area, diesel];
    const pythonProcess = spawn('python', [pythonScriptPath, ...args]);

    pythonProcess.stdout.on('data', (data) => {
      // console.log(${data});
      console.log(data.toString());
    });

    // let options={
    //   args:[file1Path,file2Path,district,area,diesel]
    // }
    // PythonShell.run("C:/FYP/myNode/test.py",options,function(err,results){
    //   console.log(results)
    // })

    // pythonScript.on('close', (code) => {
    //   rl.close();
    // });
    res.json({ success: true });
  });
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
