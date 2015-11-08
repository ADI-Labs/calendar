'use strict';

var webpack = require('webpack'),  
  HtmlWebpackPlugin = require('html-webpack-plugin'),
  path = require('path'),
  srcPath = path.join(__dirname, 'cal/src');

module.exports = {  
  target: 'web',
  cache: true,
  entry: {
    app: path.join(srcPath, 'index.js'),
    common: ['react', 'react-dom', 'react-router', 'alt']
  },
  resolve: {
    root: srcPath,
    extensions: ['', '.js'],
    modulesDirectories: ['node_modules', 'cal/src']
  },
  output: {
    path: path.join(__dirname, 'cal/tmp'),
    publicPath: '',
    filename: '[name].js',
    library: ['Example', '[name]'],
    pathInfo: true
  },

  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      }
    ]
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin('common', 'common.js'),
    new HtmlWebpackPlugin({
      inject: true,
      template: 'cal/templates/index.html'
    }),
    new webpack.NoErrorsPlugin()
  ],

  debug: true,
  devtool: 'eval-cheap-module-source-map',
  devServer: {
    contentBase: './cal/tmp',
    historyApiFallback: true
  }
};




  // module: {
  //   loaders: [
  //     {test: /\.js?$/, exclude: /node_modules/, loader: 'babel?cacheDirectory'}
  //   ]
  // },


