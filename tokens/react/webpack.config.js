var webpack = require('webpack');

module.exports = {
  entry: ['babel-polyfill', './index.js'],
  module: {
    loaders: [
      {
        test: /\.(js|jsx)$/,
        loader: 'babel',
        exclude: [/node_modules/, /__tests__/],
        query: {
          plugins: ['transform-decorators-legacy'],
          presets: ['es2015', 'stage-0', 'react'],
        },
      },
      {
        test: /\.css$/,
        loader: "style-loader!css-loader",
      },
      {
        test: /\.json$/,
        loader: "json-loader",
      },
      {
        test: /\.yjsx$/,
        loader: [
          'babel?presets[]=es2015,presets[]=stage-0,presets[]=react',
          'yjsx-loader',
        ],
      },
    ],
  },
  output: {
    path: './static',
    filename: 'bundle.js',
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin({
      minimize: true,
      compress: {
        warnings: false,
      },
    }),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"production"',
    }),
    new webpack.ProvidePlugin({
      React: "react",
    }),
  ],
};
