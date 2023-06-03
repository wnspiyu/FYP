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
    const buildings = req.body.numBuildings;
    const dimensions = req.body.dimensionsArray;
    const district = req.body.district;
    const file1path = files[0].path;
    const file2path = files[1].path;
    const file3path = files[2].path;

    const pythonScriptPath = path.join(__dirname,'test.py');
    const args = [file1path, file2path, file3path,buildings,dimensions,district];
    const pythonProcess = spawn('python', [pythonScriptPath, ...args]);

    var outputData;

    pythonProcess.stdout.on('data', async (data) => {
      outputData = JSON.parse(data);
      console.log(outputData);
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
    
});

app.post('/optimize', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to upload files' });
    }
    const target = req.body.target;
    const dimensions = JSON.parse(req.body.dimensionsArray);
    const district = req.body.district;
    const Total_EM =req.body.Total_EM;
    const Grid_EM =req.body.Grid_EM;
    const diesel_emission =req.body.diesel_emission;
    const Fuel_oil_EM =req.body.Fuel_oil_EM;
    
    const pythonScriptPath1 = path.join(__dirname,'test3.py');
    const args1 = [target, dimensions, district,Total_EM,Grid_EM,diesel_emission,Fuel_oil_EM];
    const pythonProcess1 = spawn('python', [pythonScriptPath1, ...args1]);

    var outputData1;

    pythonProcess1.stdout.on('data', async (data) => {
      outputData1 = JSON.parse(data);
      console.log(outputData1);
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
