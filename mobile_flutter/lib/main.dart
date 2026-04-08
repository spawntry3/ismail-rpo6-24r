import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

/// `null` — ПК и Android-эмулятор; для телефона в Wi‑Fi: `http://192.168.x.x:8000`.
const String? kApiHostOverride = null;

void main() {
  runApp(const AdsApp());
}

class AdsApp extends StatelessWidget {
  const AdsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'KaspiBoard Mobile',
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFFDC2626),
        useMaterial3: true,
      ),
      home: const AdsFeedPage(),
    );
  }
}

class AdItem {
  final String uuid;
  final String title;
  final String description;
  final int price;
  final bool isTop;
  final String imageUrl;
  final String category;
  final String city;
  final String author;

  AdItem({
    required this.uuid,
    required this.title,
    required this.description,
    required this.price,
    required this.isTop,
    required this.imageUrl,
    required this.category,
    required this.city,
    required this.author,
  });

  factory AdItem.fromJson(Map<String, dynamic> json) {
    return AdItem(
      uuid: json['uuid'] as String,
      title: json['title'] as String,
      description: json['description'] as String? ?? '',
      price: json['price'] as int? ?? 0,
      isTop: json['is_top'] as bool? ?? false,
      imageUrl: json['image_url'] as String? ?? '',
      category: json['category'] as String? ?? '',
      city: json['city'] as String? ?? '',
      author: json['author'] as String? ?? '',
    );
  }
}

class AdsApi {
  /// Эмулятор Android → 10.0.2.2; симулятор iOS / Windows → localhost.
  /// Реальный телефон → задай [kApiHostOverride] и `runserver 0.0.0.0:8000`.
  static String get baseUrl {
    final override = kApiHostOverride?.trim();
    if (override != null && override.isNotEmpty) {
      return override.replaceAll(RegExp(r'/+$'), '');
    }
    if (kIsWeb) return 'http://127.0.0.1:8000';
    if (defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000';
    }
    return 'http://127.0.0.1:8000';
  }

  static Future<List<AdItem>> fetchAds() async {
    final response = await http.get(Uri.parse('${baseUrl}/api/ads/'));
    if (response.statusCode != 200) {
      throw Exception('Failed to load ads: ${response.statusCode}');
    }
    final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
    return data
        .map((item) => AdItem.fromJson(item as Map<String, dynamic>))
        .toList();
  }
}

class AdsFeedPage extends StatefulWidget {
  const AdsFeedPage({super.key});

  @override
  State<AdsFeedPage> createState() => _AdsFeedPageState();
}

class _AdsFeedPageState extends State<AdsFeedPage> {
  late Future<List<AdItem>> _futureAds;

  @override
  void initState() {
    super.initState();
    _futureAds = AdsApi.fetchAds();
  }

  Future<void> _refresh() async {
    setState(() {
      _futureAds = AdsApi.fetchAds();
    });
    await _futureAds;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Лента объявлений')),
      body: FutureBuilder<List<AdItem>>(
        future: _futureAds,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Text('Ошибка загрузки: ${snapshot.error}'),
              ),
            );
          }
          final ads = snapshot.data ?? <AdItem>[];
          if (ads.isEmpty) {
            return const Center(child: Text('Объявлений пока нет'));
          }

          return RefreshIndicator(
            onRefresh: _refresh,
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: ads.length,
              itemBuilder: (context, index) {
                final ad = ads[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(
                    side: BorderSide(
                      color: ad.isTop ? const Color(0xFFFFB84A) : Colors.transparent,
                      width: ad.isTop ? 2 : 0,
                    ),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (ad.imageUrl.isNotEmpty)
                        ClipRRect(
                          borderRadius: const BorderRadius.vertical(top: Radius.circular(14)),
                          child: Image.network(
                            ad.imageUrl,
                            width: double.infinity,
                            height: 170,
                            fit: BoxFit.cover,
                            errorBuilder: (_, __, ___) => const SizedBox.shrink(),
                          ),
                        ),
                      Padding(
                        padding: const EdgeInsets.all(12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            if (ad.isTop)
                              Container(
                                margin: const EdgeInsets.only(bottom: 8),
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                decoration: BoxDecoration(
                                  color: const Color(0xFFFFF1D9),
                                  borderRadius: BorderRadius.circular(999),
                                ),
                                child: const Text('💎 VIP', style: TextStyle(fontWeight: FontWeight.w700)),
                              ),
                            Text(ad.title, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
                            const SizedBox(height: 6),
                            Text(
                              ad.price == 0 ? 'Бесплатно' : '${ad.price} ₸',
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w800,
                                color: Color(0xFFDC2626),
                              ),
                            ),
                            const SizedBox(height: 6),
                            Text('${ad.city} • ${ad.category} • ${ad.author}', style: const TextStyle(color: Colors.black54)),
                            const SizedBox(height: 6),
                            Text(
                              ad.description,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(color: Colors.black87),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
