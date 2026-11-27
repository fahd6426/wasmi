#!/bin/bash
# يضبط مشروع iOS بعد ما ينبني: صلاحيات الموقع، العمل بالخلفية، رابط wasmii://، الاسم واللغة
set -e
PL=ios/App/App/Info.plist
B=/usr/libexec/PlistBuddy
set_s(){ $B -c "Delete :$1" "$PL" 2>/dev/null || true; $B -c "Add :$1 string $2" "$PL"; }
set_s CFBundleDisplayName "وسمي"
set_s CFBundleDevelopmentRegion "ar"
set_s NSLocationWhenInUseUsageDescription "نستخدم موقعك عشان نوريك مكانك بالخريطة، ونوجّهك للمكان اللي تبيه، ونحسب نسبة الربيع حولك."
set_s NSLocationAlwaysAndWhenInUseUsageDescription "عشان قارمن وسمي يكمّل يسجّل جرتك ويوجّهك وأنت بالبر حتى لو قفلت الشاشة."
set_s NSLocationAlwaysUsageDescription "عشان قارمن وسمي يكمّل يسجّل جرتك ويوجّهك وأنت بالبر حتى لو قفلت الشاشة."
set_s NSMotionUsageDescription "نستخدم بوصلة الجوال عشان الخريطة تلف مع اتجاهك."
$B -c "Delete :UIBackgroundModes" "$PL" 2>/dev/null || true
$B -c "Add :UIBackgroundModes array" "$PL"
$B -c "Add :UIBackgroundModes:0 string location" "$PL"
$B -c "Delete :CFBundleURLTypes" "$PL" 2>/dev/null || true
$B -c "Add :CFBundleURLTypes array" "$PL"
$B -c "Add :CFBundleURLTypes:0 dict" "$PL"
$B -c "Add :CFBundleURLTypes:0:CFBundleURLName string com.wasmii.app" "$PL"
$B -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes array" "$PL"
$B -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes:0 string wasmii" "$PL"
$B -c "Delete :ITSAppUsesNonExemptEncryption" "$PL" 2>/dev/null || true
$B -c "Add :ITSAppUsesNonExemptEncryption bool false" "$PL"
# آيفون بس (بدون آيباد)
sed -i '' 's/TARGETED_DEVICE_FAMILY = "1,2";/TARGETED_DEVICE_FAMILY = 1;/g' ios/App/App.xcodeproj/project.pbxproj
echo "Info.plist جاهز"
