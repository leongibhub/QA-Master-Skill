const {defineConfig}=require('cypress');
module.exports=defineConfig({e2e:{baseUrl:'http://127.0.0.1:4173',specPattern:'checkout.cy.js',supportFile:false},video:false,retries:0});
