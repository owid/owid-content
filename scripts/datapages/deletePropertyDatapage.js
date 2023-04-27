const fs = require('fs');
const path = require('path');

// Usage: node deletePropertyDatapage.js Removes a property from all datapage
// JSONs in the datapages folder. Can also be used to format JSONs by using an
// empty propertyNameToDelete.

const propertyNameToDelete = 'anomaliesListText'; // The name of the property to delete

const folderPath = path.join(__dirname, "../../datapages");

fs.readdir(folderPath, (err, files) => {
  if (err) {
    console.log(err);
    return;
  }

  files.forEach((file) => {
    if (path.extname(file) === '.json') { // Only process JSON files
      const filePath = path.join(folderPath, file);

      fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
          console.log(err);
          return;
        }

        let json = JSON.parse(data);
        delete json[propertyNameToDelete]; // Delete the property from the JSON object
        const jsonString = JSON.stringify(json, null, 4);

        fs.writeFile(filePath, jsonString, 'utf8', (err) => {
          if (err) {
            console.log(err);
            return;
          }

          console.log(`Deleted property "${propertyNameToDelete}" from file: ${filePath}`);
        });
      });
    }
  });
});
