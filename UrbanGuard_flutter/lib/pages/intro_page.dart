import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:urban_guard/pages/register_camera_page.dart';
import 'package:url_launcher/url_launcher.dart';

class IntroPage extends StatelessWidget {
  const IntroPage({super.key});

  Future<void> _redirectToGitHub() async {
    final Uri url = Uri.parse('https://github.com/divakar02');
    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[50],
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue[100]!, Colors.blue[400]!],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Column(
          children: [
            // Header Section
            Container(
              padding: EdgeInsets.only(top: 60),
              child: Column(
                children: [
                  SizedBox(
                    height: 25,
                  ),
                  Text(
                    'URBAN GUARD',
                    style: GoogleFonts.montserrat(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue[800],
                    ),
                  ),
                  InkWell(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => RegisterCameraPage(), // Replace SecondPage with your desired page
                        ),
                      );
                    },
                    child: Lottie.asset('assets/lottie/DoomCCTV.json',
                        width: 150, height: 150),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      'S3R AI-Driven Crime Detection and Prevention System, Specialized for Proactive Woman Safety',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.montserrat(
                        fontSize: 14,
                        color: Colors.blueGrey,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            // Carousel Section
            Expanded(
              child: CarouselSlider(
                items: [
                  buildCarouselItem(
                      'The Problem?',
                      'Delays in detecting crimes risk lives.',
                      'assets/lottie/Emergency.json'),
                  buildCarouselItem(
                      'The Strategy!',
                      'AI for real-time detection and alerts.',
                      'assets/lottie/CustomerSupport.json'),
                  buildCarouselItem(
                      'The Revolution!<3',
                      'Saving lives and protecting property.',
                      'assets/lottie/DataAnalyst.json'),
                ],
                options: CarouselOptions(
                  autoPlay: true,
                  enlargeCenterPage: true,
                  aspectRatio: 15 / 11,
                ),
              ),
            ),
            // Footer Section
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  ElevatedButton(
                    onPressed: _redirectToGitHub,
                    child: Text(
                      'Redirect to GIT',

                      style: GoogleFonts.montserrat(color: Colors.blue[800] ),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => RegisterCameraPage(), // Replace SecondPage with your desired page
                        ),
                      );
                    },
                    child: Text(
                      'Start Processing',
                      style: GoogleFonts.montserrat(color: Colors.blue[800]),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildCarouselItem(String title, String description, String assetPath) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 8),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.6),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1), // Slight opacity shadow
            blurRadius: 8,
            spreadRadius: 2,
            offset: Offset(0, 4), // Subtle downward shadow
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Lottie.asset(assetPath, width: 70, height: 120),
          SizedBox(height: 10),
          Text(
            title,
            style: GoogleFonts.montserrat(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 5),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              description,
              textAlign: TextAlign.center,
              style: GoogleFonts.montserrat(
                fontSize: 16,
                color: Colors.blueGrey,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
