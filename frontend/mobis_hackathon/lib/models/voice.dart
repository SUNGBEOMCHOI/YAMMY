import 'dart:io';
import 'package:path/path.dart';

String basePath = '';

class Voice {
  late String fullPath;
  late String fileName;

  Voice(this.fullPath) {
    File file = File(fullPath);
    fileName = basename(file.path);
  }
}
