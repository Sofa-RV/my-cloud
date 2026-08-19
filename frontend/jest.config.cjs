module.exports = {
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest"
  },
  setupFilesAfterEnv: [
    "<rootDir>/src/setupTests.js"
  ],
  moduleFileExtensions: [
    "js",
    "jsx"
  ],
  testMatch: [
    "<rootDir>/src/**/*.test.jsx",
    "<rootDir>/src/**/*.test.js"
  ],
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "<rootDir>/src/testStyleMock.js"
  }
};
