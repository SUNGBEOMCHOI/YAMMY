import 'package:flutter/material.dart';
import 'package:mobis_hackathon/screen/record_screen.dart';

class FirstScreen extends StatefulWidget {
  const FirstScreen({super.key});

  @override
  State<FirstScreen> createState() => _FirstScreenState();
}

class _FirstScreenState extends State<FirstScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(milliseconds: 3000), () {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => (const RecordScreen()),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    const String imageLogoName = 'assets/images/yai로고.png';

    var screenHeight = MediaQuery.of(context).size.height;
    var screenWidth = MediaQuery.of(context).size.width;

    return WillPopScope(
      onWillPop: () async => false,
      child: MediaQuery(
        data: MediaQuery.of(context).copyWith(textScaleFactor: 1.0),
        child: Scaffold(
          backgroundColor: Theme.of(context).backgroundColor,
          body: Container(
            alignment: Alignment.center,
            child: Image.asset(
              imageLogoName,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }
}
