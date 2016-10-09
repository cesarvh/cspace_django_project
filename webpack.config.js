/* eslint import/no-extraneous-dependencies: "off" */

const webpack = require('webpack');

const library = 'webappstuff';
/* const env = process.env.NODE_ENV;
 const isProduction = env === 'production'; */
const isProduction = true;

const config = {
    entry: './client_modules/js/app.js',
    output: {
        path: './webpack_dist',
        filename: 'app.bundle.js',
        library: library,
        libraryTarget: 'umd'
    },
    module: {
        loaders: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                loader: 'babel',
            },
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery",
            d3: 'd3'
        }),
    ],
    resolve: {
        extensions: ['', '.js', '.jsx'],
    },
};

if (isProduction) {
    config.plugins.push(
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false,
            },
            output: {
                comments: false,
            },
        })
    );
}

module.exports = config;
