#include <bits/stdc++.h> 

using namespace std;
int normalizeShift(int shift) {

    return (shift % 26 + 26) % 26;
}
string caesarEncrypt(string text, int shift) {
    string result = ""; // Chuỗi kết quả
    int normalizedShift = normalizeShift(shift);
    for (char c : text) {
        if (isalpha(c)) {
            char base = isupper(c) ? 'A' : 'a';
            char shifted_char = static_cast<char>((c - base + normalizedShift) % 26 + base);
            
            result += shifted_char;
        } else {
            result += c;
        }
    }
    return result;
}
string caesarDecrypt(string text, int shift) {
    return caesarEncrypt(text, -shift);
}
int main() {
    string plaintext;
    int shift;
    cout << "===== MA HOA CAESAR =====" << endl;
    cout << "Nhap van ban goc: ";
    getline(cin, plaintext);
    cout << "Nhap khoa (so buoc dich): ";
    cin >> shift;
    string ciphertext = caesarEncrypt(plaintext, shift);
    cout << "--------------------------" << endl;
    cout << "Van ban da ma hoa: " << ciphertext << endl;
    string decryptedText = caesarDecrypt(ciphertext, shift);
    cout << "Van ban da giai ma: " << decryptedText << endl;
    return 0;
}