import 'package:flutter/material.dart';
import 'package:mobis_hackathon/screen/first_screen.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
    return MaterialApp(
        home: const FirstScreen(),
        theme: ThemeData(
          backgroundColor: const Color(0xff7E81EB),
          canvasColor: const Color(0xff000000).withAlpha(110),
          cardColor: const Color.fromARGB(255, 206, 233, 238),
          fontFamily: 'Leferi',
          textTheme: const TextTheme(
            headline2: TextStyle(
              fontSize: 24.0,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
            subtitle1: TextStyle(
              fontSize: 20.0,
              fontWeight: FontWeight.bold,
              color: Color(0xff4f4f4f),
            ),
            bodyText1: TextStyle(
              fontSize: 30.0,
              color: Colors.black,
            ),
            bodyText2: TextStyle(
              fontSize: 14.0,
              color: Colors.white,
            ),
          ),
        ));
  }
}
