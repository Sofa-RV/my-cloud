const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: path.resolve(
    __dirname,
    "src",
    "index.jsx",
  ),

  output: {
    path: path.resolve(
      __dirname,
      "dist",
    ),
    filename: "assets/js/[name].[contenthash].js",
    clean: true,
    publicPath: "/",
  },

  resolve: {
    extensions: [
      ".js",
      ".jsx",
    ],
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/i,
        use: [
          "style-loader",
          "css-loader",
        ],
      },
    ],
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(
        __dirname,
        "public",
        "index.html",
      ),
      title: "My Cloud",
    }),
  ],

  devServer: {
    port: 3000,
    open: true,
    hot: true,
    historyApiFallback: true,

    static: {
      directory: path.resolve(
        __dirname,
        "public",
      ),
    },
  },

  devtool: "source-map",
};