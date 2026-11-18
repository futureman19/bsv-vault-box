'use strict';
const path=require('node:path');
const esbuild=require('esbuild');
Promise.all(['browser-wallet','browser-wallet-fixture'].map(name=>esbuild.build({entryPoints:[path.join(__dirname,name+'.js')],outfile:path.join(__dirname,name+'.bundle.js'),bundle:true,platform:'browser',format:'iife',target:['es2020'],minify:true,legalComments:'eof'}))).catch(e=>{console.error(e);process.exitCode=1;});
