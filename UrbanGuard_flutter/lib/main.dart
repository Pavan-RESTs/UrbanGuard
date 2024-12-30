import 'package:flutter/material.dart';
import 'package:urban_guard/pages/intro_page.dart';
import 'pages/onboarding_page.dart';

void main() {
  runApp(UrbanGuardApp());
}

class UrbanGuardApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'UrbanGuard',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: IntroPage(),
    );
  }
}
