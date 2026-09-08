import datetime,importlib.util,pathlib,unittest
s=importlib.util.spec_from_file_location('news',pathlib.Path(__file__).resolve().parents[1]/'scripts/update_news.py');n=importlib.util.module_from_spec(s);s.loader.exec_module(n)
class NewsTests(unittest.TestCase):
 def test_mentions(self):
  self.assertEqual(n.mentions('Talk to us about this'),[]);self.assertEqual(n.mentions('US and China sign agreement'),['USA','CHN']);self.assertEqual(n.mentions('Rusia y Corea del Norte'),['RUS','PRK'])
 def test_feed_dates(self):
  now=datetime.datetime(2026,9,8,tzinfo=datetime.timezone.utc)
  def feed(date,url='https://example.com/story'):
   return f'<rss><channel><item><title>China talks with US</title><link>{url}</link><pubDate>{date}</pubDate></item></channel></rss>'
  self.assertEqual(len(n.parse_feed(feed('Mon, 07 Sep 2026 12:00:00 GMT'),'test',now)),1)
  self.assertEqual(n.parse_feed(feed('Wed, 09 Sep 2026 12:00:00 GMT'),'test',now),[])
  self.assertEqual(n.parse_feed(feed('Sat, 01 Aug 2026 12:00:00 GMT'),'test',now),[])
  self.assertEqual(n.parse_feed(feed('Mon, 07 Sep 2026 12:00:00 GMT','javascript:alert(1)'),'test',now),[])
if __name__=='__main__':unittest.main()
