
// const { spawn } = require('child_process');
// const readline = require('readline');

// const rl = readline.createInterface({
//   input: process.stdin,
//   output: process.stdout
// });

// rl.question('Enter path to Excel file 1: ', (file1Path) => {
//   rl.question('Enter path to Excel file 2: ', (file2Path) => {
//     const pythonScript = spawn('python', ["C:/FYP/myNode/test.py", file1Path, file2Path]);

//     pythonScript.stdout.on('data', (data) => {
//       // console.log(`stdout: ${data}`);
//       console.log(`${data}`);
//     });

//     // pythonScript.stderr.on('data', (data) => {
//     //   console.error(`stderr: ${data}`);
//     // });

//     pythonScript.on('close', (code) => {
//       //console.log(`child process exited with code ${code}`);
//       rl.close();
//     });
//   });
// });

// const { spawn } = require('child_process');
// const readline = require('readline');

// const rl = readline.createInterface({
//   input: process.stdin,
//   output: process.stdout
// });

// const file1Path = "uploads\\Scaled data from Imported electricity- dan.xlsx";
// const file2Path = "uploads\\Scaled steam demand data.xlsx";
// const area = 200;
// const diesel = 5000;
// const district = "Gampaha";

// const pythonScript = spawn('python', ["C:/FYP/myNode/test.py", file1Path, file2Path,district,area,diesel]);

// pythonScript.stdout.on('data', (data) => {
//   //console.log(`stdout: ${data}`);
//   console.log(`${data}`);
// });

// // pythonScript.stderr.on('data', (data) => {
// //   console.error(`stderr: ${data}`);
// // });

// pythonScript.on('close', (code) => {
//   //console.log(`child process exited with code ${code}`);
//   rl.close();
// });
const { spawn } = require('child_process');
//const readline = require('readline');
const path = require('path');
// const rl = readline.createInterface({
//   input: process.stdin,
//   output: process.stdout
// });

const file1path = "uploads\\Scaled data from Imported electricity- dan.xlsx";
const file2path = "uploads\\Scaled steam demand data.xlsx";
const district = "Gampaha";
const area = 200;
const diesel = 5000;


// console.log("Executing Python script with the following inputs:");
// console.log(`file1Path: ${file1Path}`);
// console.log(`file2Path: ${file2Path}`);
// console.log(`area: ${area}`);
// console.log(`diesel: ${diesel}`);
// console.log(`district: ${district}`);

const pythonScriptPath = path.join(__dirname,'test.py');
const args = [file1path, file2path, district, area, diesel];
const pythonProcess = spawn('python', [pythonScriptPath, ...args]);

pythonProcess.stdout.on('data', (data) => {
  // console.log(${data});
  console.log(data.toString());
});

// pythonProcess.stderr.on('data', (data) => {
//   console.error(`stderr: ${data}`);
// });

// pythonProcess.on('close', (code) => {
//   console.log(`child process exited with code ${code}`);
// });