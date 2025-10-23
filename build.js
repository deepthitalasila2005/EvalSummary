const fs = require('fs');
const path = require('path');

// Create dist directory if it doesn't exist
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir);
}

// Files and directories to copy
const filesToCopy = [
    'index.html',
    'style.css', 
    'script.js',
    'staticwebapp.config.json'
];

const htmlFiles = fs.readdirSync('.').filter(file => 
    file.endsWith('.html') && file !== 'index.html'
);

// Copy individual files
filesToCopy.forEach(file => {
    if (fs.existsSync(file)) {
        fs.copyFileSync(file, path.join(distDir, file));
        console.log(`Copied ${file}`);
    }
});

// Copy all HTML report files
htmlFiles.forEach(file => {
    fs.copyFileSync(file, path.join(distDir, file));
    console.log(`Copied ${file}`);
});

console.log('Build completed successfully!');