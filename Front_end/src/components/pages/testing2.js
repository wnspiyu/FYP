const express = require('express');
const cors = require('cors'); // Import the cors middleware
const fs = require('fs');
const xlsx = require('xlsx');
const bodyParser = require('body-parser');

const app = express();
const port = 3100;

app.use(cors({
    origin: 'http://localhost:3000', // Allow requests from http://localhost:3000
    optionsSuccessStatus: 200
  }));
app.use(bodyParser.json({ limit: '50mb' }));
app.use(express.json());
app.use(express.static('public'));

let worksheet = xlsx.utils.aoa_to_sheet([
    ['', ''],
    ['', 0],
    ['', 0],
  ]);

app.post('/upload', (req, res) => {
  const base64String = req.body.data;
  const arrayBuffer = Buffer.from(base64String, 'base64');
  const workbook = xlsx.read(arrayBuffer, { type: 'buffer' });
  worksheet = workbook.Sheets[workbook.SheetNames[0]];
  const data = xlsx.utils.sheet_to_json(worksheet, { header: 1 });
  console.log(data);


   //
// Create a new workbook
const workbook2 = xlsx.utils.book_new();

// Add the worksheet to the workbook
xlsx.utils.book_append_sheet(workbook2, worksheet, 'Sheet1');

// Write the workbook to a file
const buffer = xlsx.write(workbook2, { bookType: 'xlsx', type: 'buffer' });
fs.writeFileSync('public/example.xlsx', buffer);

console.log('File written successfully!');



  // process the data as needed
  res.send({ success: true });
});

app.listen(port, () => {
   console.log(`App listening at http://localhost:${port}`);

});