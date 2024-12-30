import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:urban_guard/pages/video_upload_page.dart';

class RegisterCameraPage extends StatefulWidget {
  @override
  _RegisterCameraPageState createState() => _RegisterCameraPageState();
}

class _RegisterCameraPageState extends State<RegisterCameraPage> {
  String? _selectedLocality;
  final Map<String, List<double>> localityCoordinates = {
    'Anna Salai': [13.0827, 80.2716],
    'Mylapore': [13.0333, 80.2674],
    'T. Nagar': [13.0416, 80.2337],
    'Velachery': [12.9792, 80.2183],
    'Adyar': [13.0067, 80.2577],
    'Egmore': [13.0787, 80.2603],
    'Perungudi': [12.9682, 80.2489],
    'Royapettah': [13.0555, 80.2646],
    'Guindy': [13.0075, 80.2205],
    'Kodambakkam': [13.0525, 80.2304],
  };


  String? _coordinates;

  void _goToNextPage() {
    if (_selectedLocality != null) {
      final coordinates = localityCoordinates[_selectedLocality];
      _coordinates = '${coordinates![0]}, ${coordinates[1]}';

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => VideoUploadPage(
            _selectedLocality!,
            _coordinates!,
          ),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please select a locality first!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue[100]!, Colors.blue[400]!],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                AppBar(
                  backgroundColor: Colors.transparent,
                  elevation: 0,
                  centerTitle: true,
                  title: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.security, color: Colors.white, size: 24),
                      SizedBox(width: 8),
                      Text(
                        'Urban Guard',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        SizedBox(height: 20),
                        Lottie.asset(
                          'assets/lottie/GlobalGPS.json',
                          height: 200,
                          repeat: true,
                          animate: true,
                        ),
                        SizedBox(height: 20),
                        Card(
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(15),
                          ),
                          elevation: 5,
                          margin: EdgeInsets.symmetric(horizontal: 10),
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Camera Registration',
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.blue[800],
                                  ),
                                ),
                                SizedBox(height: 10),
                                Text(
                                  'Please select the locality of your CCTV:',
                                  style: TextStyle(
                                    fontSize: 14,
                                    color: Colors.black87,
                                  ),
                                ),
                                SizedBox(height: 20),
                                DropdownButtonFormField<String>(
                                  value: _selectedLocality,
                                  hint: Text(
                                    'Select a Locality',
                                    style: TextStyle(
                                      color: Colors.blueGrey,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  icon: Icon(Icons.arrow_drop_down,
                                      color: Colors.blue[800]),
                                  onChanged: (String? newValue) {
                                    setState(() {
                                      _selectedLocality = newValue;
                                    });
                                  },
                                  items: localityCoordinates.keys
                                      .map<DropdownMenuItem<String>>(
                                          (String value) {
                                        return DropdownMenuItem<String>(
                                          value: value,
                                          child: Text(value,
                                              style: TextStyle(
                                                  color: Colors.blue[800])),
                                        );
                                      }).toList(),
                                ),
                                SizedBox(height: 20),
                                if (_selectedLocality != null)
                                  Column(
                                    crossAxisAlignment:
                                    CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Selected Locality: $_selectedLocality',
                                        style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.blue[800],
                                        ),
                                      ),
                                      SizedBox(height: 5),
                                      Text(
                                        'Coordinates: ${localityCoordinates[_selectedLocality]?.join(", ")}',
                                        style: TextStyle(
                                          fontSize: 14,
                                          color: Colors.blue[700],
                                        ),
                                      ),
                                    ],
                                  ),
                              ],
                            ),
                          ),
                        ),
                        SizedBox(height: 30),
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blue[800],
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(30),
                            ),
                            padding: EdgeInsets.symmetric(
                                vertical: 12, horizontal: 40),
                          ),
                          onPressed: _goToNextPage,
                          child: Text(
                            'Next',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

void main() => runApp(MaterialApp(home: RegisterCameraPage()));
