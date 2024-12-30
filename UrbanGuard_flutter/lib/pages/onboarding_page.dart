import 'package:flutter/material.dart';
import 'register_camera_page.dart';
import 'package:liquid_swipe/liquid_swipe.dart';

class OnboardingPage extends StatelessWidget {
  final pages = [
    Container(color: Colors.blue, child: Center(child: Text('Welcome to UrbanGuard', style: TextStyle(fontSize: 24, color: Colors.white)))),
    Container(color: Colors.red, child: Center(child: Text('Monitor Locations Safely', style: TextStyle(fontSize: 24, color: Colors.white)))),
    Container(color: Colors.green, child: Center(child: Text('Stay Alert, Stay Safe', style: TextStyle(fontSize: 24, color: Colors.white)))),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(

      body: LiquidSwipe(
        pages: pages,
        fullTransitionValue: 600,
        waveType: WaveType.circularReveal,
        onPageChangeCallback: (index) {
          if (index == pages.length - 1) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => RegisterCameraPage()),
            );
          }
        },
      ),
    );
  }
}
