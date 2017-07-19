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
      {
        enforce: "pre",
        test: /\.js$/,
        loader: "eslint-loader",
        exclude: /node_modules/,
      },
    ],
  },
  output: {
    path: './static',
    filename: 'bundle.js',
  },
  plugins: [
    new webpack.ProvidePlugin({
      React: "react",
    }),
  ],
};
