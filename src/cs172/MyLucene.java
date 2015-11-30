package cs172;
import java.io.*;
import java.util.StringTokenizer;
import java.util.Scanner;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;


class TweetDoc {
	public String date;
	public String coords;
	public String user;
	public String text;
	public String hashtags;
	public String link;
	public String ptitle;
	
	TweetDoc(String d, String c, String u, String t, String h, String l, String p) {
		this.date = d;
		this.coords = c;
		this.user = u;
		this.text = t;
		this.hashtags = h;
		this.link = l;
		this.ptitle = p;
	}
	
}

public class MyLucene {
	public static final String INDEX_DIR = "testIndex";
	public static void main(String[] args) throws CorruptIndexException, IOException {
		
		
	
		
		if (args.length == 0) {
		
		//READ FROM FILES
		BufferedReader reader = null;
        int count = 0;
        int file_no = 0;
		
        try {
        	File file = new File("data/twitter_data"+file_no+".txt");
        	
        	while (file.exists()) {
        	
	        	System.out.println("Reading from file '" + file + "'...");
	            reader = new BufferedReader(new FileReader(file));
	            
	            // Read every line in the file, and parse each tweet.
	            for (String line; (line = reader.readLine()) != null; ) {
	            	count++; //Count number of tweets
	            	System.out.println("Tweets = " + count);
	                Scanner s = new Scanner(line).useDelimiter("\\s*Date:\\s*|\\s*Coords:\\s*|\\s*User:\\s*|\\s*Text:\\s*|\\s*Hashtags:\\s*|\\s*URL:\\s*|\\s*Title:\\s*");
	                String date = s.next();
	                String coords = s.next();
	                String user = s.next();
	                String text = s.next();
	                String hashtags = s.next();
	                String url = s.next();
	                String title = "";
	                if (s.hasNext()) {
	                	title = s.next();
	                }
	                
	                //Declare tweet, and index it in Lucene
	                TweetDoc tweet1 = new TweetDoc(date, coords, user, text, hashtags, url, title);    
	                index(tweet1);
	            }
	            
	            reader.close();
	            System.out.println("Current number of tweets = " + count);
	            file_no++;
	            file = new File("data/twitter_data"+file_no+".txt");
            
        	}
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            try {
                reader.close();
                System.out.println("Total number of tweets = " + count);
            }
            catch (IOException e) {
                e.printStackTrace();
            }

        } 
        
		}
		
		
		
		
	}
		
    
    public static void index (TweetDoc tweet) {
    	File index = new File(INDEX_DIR);
    	IndexWriter writer = null;
    	
    	try {	
			IndexWriterConfig indexConfig = new IndexWriterConfig(Version.LUCENE_34, new StandardAnalyzer(Version.LUCENE_35));
			writer = new IndexWriter(FSDirectory.open(index), indexConfig);
			Document luceneDoc = new Document();
			luceneDoc.add(new Field("date", tweet.date, Field.Store.YES, Field.Index.NO));
			luceneDoc.add(new Field("user", tweet.user, Field.Store.YES, Field.Index.NO));
			luceneDoc.add(new Field("coords", tweet.coords, Field.Store.YES, Field.Index.NO));
			luceneDoc.add(new Field("text", tweet.text, Field.Store.YES, Field.Index.ANALYZED));
			luceneDoc.add(new Field("hashtags", tweet.hashtags, Field.Store.YES, Field.Index.ANALYZED));
			luceneDoc.add(new Field("link", tweet.link, Field.Store.YES, Field.Index.NO));			
			luceneDoc.add(new Field("ptitle", tweet.ptitle, Field.Store.YES, Field.Index.ANALYZED));
			luceneDoc.setBoost((float)2.0);
			writer.addDocument(luceneDoc);			
		} catch (Exception ex) {
			ex.printStackTrace();
		} finally {
			if (writer !=null)
				try {
					writer.close();
				} catch (CorruptIndexException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
		}
    
    }
    
    public static String[] search (String queryString, int topk) throws CorruptIndexException, IOException {
		
		IndexReader indexReader = IndexReader.open(FSDirectory.open(new File(INDEX_DIR)));
		IndexSearcher indexSearcher = new IndexSearcher(indexReader);
		QueryParser queryparser = new QueryParser(Version.LUCENE_34, "text", new StandardAnalyzer(Version.LUCENE_34));

		try {
			StringTokenizer strtok = new StringTokenizer(queryString, " ~`!@#$%^&*()_-+={[}]|:;'<>,./?\"\'\\/\n\t\b\f\r");
			String querytoparse = "";
			while(strtok.hasMoreElements()) {
				String token = strtok.nextToken();
				querytoparse += "text:" + token + "^1" + "hashtags:" + token+ "^1.5" + "ptitle:" + token+"^2.0";
				//querytoparse += "text:" + token;
			}		
			Query query = queryparser.parse(querytoparse);
			//System.out.println(query.toString());
			TopDocs results = indexSearcher.search(query, topk);
			int num_results = results.scoreDocs.length;
			System.out.println(num_results);
			String[] returnTweets = new String[num_results];
			for (int i = 0; i < num_results; i++) {
				String temp = "@" + indexSearcher.doc(results.scoreDocs[i].doc).getFieldable("user").stringValue();
				String date = indexSearcher.doc(results.scoreDocs[i].doc).getFieldable("date").stringValue();
				date = date.replace("+0000", "");
				temp += ": " + indexSearcher.doc(results.scoreDocs[i].doc).getFieldable("text").stringValue();
				temp += "<br/>" + date;
				System.out.println(indexSearcher.doc(results.scoreDocs[i].doc).getFieldable("text").stringValue());
				returnTweets[i] = temp;
			}
			
			
			return returnTweets;			
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			indexSearcher.close();
		}
		return null;
	}
    
    
}
   
    
    
    
    
  

