const express = require('express');
const cors = require('cors');
const xlsx = require('xlsx');
const multer = require('multer');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 3100;

app.use(cors({
    origin: 'http://localhost:3000',
    optionsSuccessStatus: 200
}));
app.use(bodyParser.json({ limit: '50mb' }));
app.use(express.json());
app.use(express.static('public'));

// let worksheet1 = xlsx.utils.aoa_to_sheet([
//     ['', ''],
//     ['', 0],
//     ['', 0],
//   ]);
// let worksheet2 = xlsx.utils.aoa_to_sheet([
//     ['', ''],
//     ['', 0],
//     ['', 0],
//   ]);

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage }).array('files');

app.post('/upload', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to upload files' });
    }

    const files = req.files;
    

    // const workbook1 = xlsx.readFile(files[0].path);
    // worksheet1 = workbook1.Sheets[workbook1.SheetNames[0]];
    // const data1 = xlsx.utils.sheet_to_json(worksheet1, { header: 1 });

    // const workbook2 = xlsx.readFile(files[1].path);
    // worksheet2 = workbook2.Sheets[workbook2.SheetNames[0]];
    // const data2 = xlsx.utils.sheet_to_json(worksheet2, { header: 1 });

    const file1path = files[0].path;
    const file2path = files[1].path;
    const file3path = files[2].path;

    // console.log(file1path);
    // console.log(file2path);
    // console.log(file3path);
    // console.log(district);
    // console.log(buildings);
    // console.log(dimensions);
    
    const pythonScriptPath = path.join(__dirname,'test.py');
    const args = [file1path, file2path, file3path];
    const pythonProcess = spawn('python', [pythonScriptPath, ...args]);

    var outputData;

    pythonProcess.stdout.on('data', async (data) => {
      outputData = JSON.parse(data);
      console.log(outputData);
      //res.json(outputData);
      try {
        res.json({
          success: true,
          data:outputData,
        });
      } catch (error) {
        res.status(500).json({ error: 'Failed to calculate onsite emissions' });
      }
    });

    pythonProcess.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
    });
  });
    // const target = req.body.target;
    // const buildings = req.body.numBuildings;
    // const dimensions = req.body.dimensionsArray;
    // console.log(target);
    // console.log(buildings);
    // console.log(dimensions);
});
app.post('/optimize', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to upload files' });
    }

    //const files = req.files;
    //const area = req.body.area;
    //const diesel = req.body.diesel;
    //const district = req.body.district;
    const target = req.body.target;
    //const buildings = req.body.numBuildings;
    const dimensions = req.body.dimensionsArray;
    const district = req.body.district;
    const Total_EM =req.body.Total_EM;

    const pythonScriptPath1 = path.join(__dirname,'test3.py');
    const args1 = [target, dimensions, district,Total_EM];
    const pythonProcess1 = spawn('python', [pythonScriptPath1, ...args1]);

    var outputData1;

    pythonProcess1.stdout.on('data', async (data) => {
      outputData1 = JSON.parse(data);
      //outputData = (data.toString());
      console.log(outputData1);
      //res.json(outputData1);
      try {
        res.json({
          success1: true,
          data1:outputData1,
        });
      } catch (error) {
        res.status(500).json({ error: 'Failed to calculate onsite emissions' });
      }
    });

    pythonProcess1.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
    });
  });
});

    
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
