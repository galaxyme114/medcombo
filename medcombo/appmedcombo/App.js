/**
 * Medcombo App
 * http://medcombo.com
 *
 */

import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
} from 'react-native';

import {WebView} from 'react-native-webview';

const App: () => React$Node = () => {
  return (
    <WebView source={{uri:'http://www.medcombo.com'}} />
  );
};

export default App;