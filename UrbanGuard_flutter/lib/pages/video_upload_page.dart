import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:lottie/lottie.dart';
import 'package:video_player/video_player.dart';

class VideoUploadPage extends StatefulWidget {
  final String location;
  final String coordinates;
// Declare the boolean variable

  VideoUploadPage(this.location, this.coordinates);

  @override
  _VideoUploadPageState createState() => _VideoUploadPageState();
}

class _VideoUploadPageState extends State<VideoUploadPage> {
  String oversampledCrop = "center_crop";
  File? videoFile;
  VideoPlayerController? _videoController;
  bool? anomalyDetected;
  String serverUrl = 'http://192.168.184.53:5005/analyze';

  // bool isUploading = false;
  double uploadProgress = 0.0;
  double videoDuration = 0.0;

  // Pick a video from the gallery
  Future<void> _pickVideo() async {
    final pickedFile = await ImagePicker().pickVideo(source: ImageSource.gallery);
    if (pickedFile != null) {
      setState(() {
        videoFile = File(pickedFile.path);
        _videoController?.dispose();
        _videoController = VideoPlayerController.file(videoFile!)
          ..initialize().then((_) {
            setState(() {
              videoDuration = _videoController!.value.duration.inSeconds.toDouble();
            });
            _videoController!.play();
          });
      });
    }
  }

  // Simulate upload progress independently
  // Future<void> simulateUploadProgress() async {
  //   setState(() {
  //     isUploading = true;
  //     uploadProgress = 0.0;
  //   });
  //
  //   int totalDurationInMillis = (videoDuration * 1000).toInt(); // Twice the video length in milliseconds
  //   for (int i = 0; i <= totalDurationInMillis; i++) {
  //     await Future.delayed(Duration(milliseconds: 10), () {
  //       if (!isUploading) return; // Stop if upload completes early
  //       setState(() {
  //         uploadProgress = i / totalDurationInMillis;
  //       });
  //     });
  //   }
  // }

  // Upload the video to the server
  Future<void> _uploadVideo() async {
    if (videoFile == null) return;

    // setState(() {
    //   isUploading = true;
    //   uploadProgress = 0.0;
    // });
    //
    // // Run progress simulation and server upload in parallel
    // final uploadSimulation = simulateUploadProgress();

    try {
      var request = http.MultipartRequest('POST', Uri.parse(serverUrl));
      request.files.add(await http.MultipartFile.fromPath('video', videoFile!.path));
      request.fields['location'] = widget.location;
      request.fields['coordinates'] = widget.coordinates;
      request.fields['anomalyDate'] = DateTime.now().toString().split(" ")[0];
      request.fields['anomalyTime'] = TimeOfDay.now().format(context);
      request.fields['oversampledCrop'] = oversampledCrop;

      var response = await request.send();
      var responseData = await http.Response.fromStream(response);

      if (response.statusCode == 200) {
        var result = json.decode(responseData.body);
        setState(() {
          anomalyDetected = result['anomaly'];
        });
      } else {
        throw Exception('Failed to upload video');
      }
    } catch (e) {
      print('Error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      // setState(() {
      //   isUploading = false;
      //   uploadProgress = 0.0;
      // });
    }

    // await uploadSimulation; // Ensure progress completes
  }

  // Show server settings dialog
  void _showSettingsDialog() {
    String tempUrl = serverUrl;
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
          title: Text(
            'Settings',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
          ),
          content: TextField(
            onChanged: (value) => tempUrl = value,
            controller: TextEditingController(text: serverUrl),
            decoration: InputDecoration(
              labelText: 'Server URL',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Cancel', style: TextStyle(color: Colors.grey)),
            ),
            ElevatedButton(
              onPressed: () {
                setState(() => serverUrl = tempUrl);
                Navigator.pop(context);
              },
              child: Text('Save'),
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    _videoController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text(
          'Urban Guard',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        backgroundColor: Colors.blueAccent,
        actions: [
          IconButton(
            icon: Icon(Icons.settings,color: oversampledCrop=="center_crop"?Colors.black : Colors.black54),
            onPressed: _showSettingsDialog,
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                'Upload Video for Anomaly Detection',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.blueGrey,
                ),
              ),
              SizedBox(height: 20),
              if (videoFile != null && _videoController != null)
                Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.grey.withOpacity(0.5),
                        spreadRadius: 3,
                        blurRadius: 7,
                        offset: Offset(0, 3),
                      ),
                    ],
                  ),
                  child: AspectRatio(
                    aspectRatio: _videoController!.value.aspectRatio,
                    child: VideoPlayer(_videoController!),
                  ),
                ),
              if (videoFile == null)
                Lottie.asset(
                  'assets/lottie/CustomerSupport.json',
                  height: 200,
                ),
              SizedBox(height: 25),
              // if (isUploading)
              //   Column(
              //     children: [
              //       LinearProgressIndicator(value: uploadProgress),
              //       SizedBox(height: 10),
              //       Text('Processing... ${(uploadProgress * 100).toInt()}%'),
              //     ],
              //   ),
              SizedBox(height: 25),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  GestureDetector(
                    onTap: _pickVideo,

                    onDoubleTap: (){
                      setState(() {
                        oversampledCrop = "10_crop";
                      });
                    },

                    onLongPress: (){
                      setState(() {
                        oversampledCrop = "center_crop";
                      });
                    },
                    child: ElevatedButton.icon(
                      onPressed: _pickVideo,
                      icon: Icon(Icons.video_library),
                      label: Text('Pick Video'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blueAccent,
                      ),
                    ),
                  ),
                  ElevatedButton.icon(
                    onPressed: _uploadVideo, //isUploading ? null :
                    icon: Icon(Icons.cloud_upload),
                    label: Text('Upload Video'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.greenAccent,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 30),
              if (anomalyDetected != null)
                AnimatedSwitcher(
                  duration: Duration(seconds: 1),
                  child: anomalyDetected!
                      ? Text('⚠️ Anomaly Detected!', style: TextStyle(color: Colors.red, fontSize: 20))
                      : Text('✅ No Anomaly Detected', style: TextStyle(color: Colors.green, fontSize: 20)),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

void main() => runApp(MaterialApp(home: VideoUploadPage('Location', 'Coordinates')));
