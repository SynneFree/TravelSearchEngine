package org.group01.travel;


import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.remote.CapabilityType;
import org.openqa.selenium.remote.DesiredCapabilities;

import com.thoughtworks.selenium.Selenium;

import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.Spider;
import us.codecraft.webmagic.downloader.HttpClientDownloader;
import us.codecraft.webmagic.processor.PageProcessor;
import us.codecraft.webmagic.proxy.Proxy;
import us.codecraft.webmagic.proxy.SimpleProxyProvider;

public class TravelProcessor implements PageProcessor
{
	// 抓取网站的相关配置，包括编码、抓取间隔、重试次数等
    private Site site = Site.me().setCycleRetryTimes(100000).setSleepTime(200).setRetrySleepTime(1000)
    		.setRetryTimes(100000).setTimeOut(10000)
    		.addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    				+ " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36")
    		;
    @Override
    public Site getSite() {
        return site;
    }

    public void process(Page page) 
    {
//    	List<Proxy> proxies = new ArrayList<>();
//    	try 
//    	{
//			proxies = buildProxyIP();
//		} 
//    	catch (IOException e) 
//    	{
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//    	Random r = new Random();
//    	
//    	System.out.println(proxies.size());
//    	int n = r.nextInt(proxies.size());
    	
//		sCaps.setCapability(CapabilityType.ForSeleniumServer.AVOIDING_PROXY, true);
//		sCaps.setCapability(CapabilityType.ForSeleniumServer.ONLY_PROXYING_SELENIUM_TRAFFIC, true);
//		System.setProperty("http.nonProxyHosts", "localhost");
//		sCaps.setCapability
//			(CapabilityType.PROXY, proxies.get(n).getHost()+":"+proxies.get(n).getPort());
//		System.out.println(proxies.get(n).getHost()+":"+proxies.get(n).getPort());
	
		
    	
        // 景区页
        if (page.getUrl().regex
        		("http(s)?://[0-9a-zA-Z]+\\.cncn\\.com/jingdian/[0-9a-zA-Z]+/profile(/)?").match()) 
        {
        	//景区名称
            page.putField("name", (page.getHtml().xpath
            		("//div[@class='city_top dj_detail']/strong/a/text()")
            		.toString()));
            System.out.println(page.getResultItems().get("name"));
            //景区评级
            page.putField("rank", (page.getHtml().xpath
            		("//div[@class='city_top dj_detail']/strong/span/text()").toString())); 
            arrange(page);
            //景区位置和地址
            String s = page.getHtml().xpath("//div[@id='bottom_address']").toString();
            int a1 = s.indexOf("地址");
            int a2 = 0;
            if(a1!=-1)
            {
                a2 = s.indexOf("[", a1);
                page.putField("position", s.substring(a1+3, a2-1));
            }
            
            a1 = s.indexOf("官网",a2);
            if(a1!=-1)
            {
            	a2 = s.indexOf("<",a1);
            	page.putField("official", s.substring(a1+3, a2-1));
            }
            //周边景点
            int i=1;
            String ar = "";
            while(page.getHtml().xpath
            		("//div[@class='txt2']/ul/li["+i+"]").toString()!=null)
            {
            	ar += page.getHtml().xpath
                		("//div[@class='txt2']/ul/li["+i+"]/span/a/text()").toString()
                		+ page.getHtml().xpath
                		("//div[@class='txt2']/ul/li["+i+"]/span/a/@href").toString()
                		+"\n";
            	i++;
            }
            page.putField("around", ar); 
            
        }
        // 主页
        else if(page.getUrl().regex
        		("http(s)?://www\\.cncn\\.com/place(/)?").match()) 
        {
        	for(int i=1;i<=29;i++)
        	{
        		int j=1;
        		while(page.getHtml().xpath
            		("//div[@class='city_all']/div["+i+"]/div[2]/a["+j+"]").toString()!=null)
        		{
        			page.addTargetRequests(page.getHtml().xpath
                    		("//div[@class='city_all']/div["+i+"]/div[2]/a["+j+"]/@href").all());
        			j++;
        		}
        	}
        }
        //景点内
        else if(page.getUrl().regex
        		("http(s)?://[0-9a-zA-Z]+\\.cncn\\.com/jingdian/[0-9a-zA-Z][')'0-9a-zA-Z'(']+(/)?").match()) 
        {
        	page.addTargetRequests(page.getHtml().xpath
            		("//dl[@class='introduce']/dd/a/@href").all());
        }
        //景点栏
        else if(page.getUrl().regex
        		("http(s)?://[0-9a-zA-Z]+\\.cncn\\.com(/[0-9a-zA-Z]*)?/jingdian(/)?(/1-[0-9]+-0-0\\.html)?")
        		.match()) 
        {
        	int i=1;
        	while(page.getHtml().xpath
            		("//div[@class='city_spots_list']/ul/li["+i+"]").toString()!=null)
        	{
        		page.addTargetRequests(page.getHtml().xpath
                		("//div[@class='city_spots_list']/ul/li["+i+"]/a/@href").all());
        		i++;
        	}
        	page.addTargetRequests(page.getHtml().xpath
            		("//div[@class='page_con']/a[@class='num next']/@href").all());
        }
        //市
        else if(page.getUrl().regex
        		("http(s)?://[0-9a-zA-Z]+\\.cncn\\.com/([0-9a-zA-Z]*)?(/)?").match()) 
        {
        	page.addTargetRequests(page.getHtml().xpath
            		("//div[@class='city_menu']/ul/li[2]/a/@href").all());
        }
        
        //99景点页面
        else if(page.getUrl().regex
        		("http(s)?://www\\.meet99\\.com/jingdian-[0-9a-zA-Z]+\\.html").match()) 
        {
        	Pspot_99.process(page);
        	page.addTargetRequests(page.getHtml().xpath
            		("//*[@id=\"jdleft\"]/div[3]/div/a/@href")
            		.all());
        }
        
        //景点下一页
        else if(page.getUrl().regex
        		("http(s)?://www\\.meet99\\.com/jingdian-[0-9a-zA-Z]+-[0-9]+\\.html").match()) 
        {
        	int n =Integer.parseInt(page.getHtml().xpath
        			("//*[@id=\"jdleft\"]/div[3]/div/b/span/text()").toString());
        	if(n<=3)
        	{
        		MysqlPipeline.updatePicture(page,n);
            	page.addTargetRequests(page.getHtml().xpath
                		("//*[@id=\"jdleft\"]/div[3]/div/a[2]/@href")
                		.all());
        	}
        }
        
        //分目录
        else if(page.getUrl().regex
        		("http(s)?://www\\.meet99\\.com/lvyou-[0-9a-zA-Z]+\\.html").match()) 
        {
        	if(page.getHtml().xpath
            		("//li[@class='open']//li[@class='open']//li[@class='open']")
            		.toString()!=null) 
        	{
        		int i=1;
            	while(page.getHtml().xpath
                		("//ul[@id='tiles']/li["+i+"]")
                		.toString()!=null)
            	{
    				page.addTargetRequests(page.getHtml().xpath
    	            		("//ul[@id='tiles']/li["+i+"]/div[2]/a/@href")
    	            		.all());
        
            		i++;
            	}
        	}
        	else
        	{
        		int i=1;
            	while(page.getHtml().xpath
                		("//li[@class='open']/ul/li[@class='open']/ul/li["+i+"]")
                		.toString()!=null)
            	{
    				page.addTargetRequests(page.getHtml().xpath
    	            		("//li[@class='open']/ul/li[@class='open']/ul/li["+i+"]/a/@href")
    	            		.all());
        
            		i++;
            	}
        	}
        }
        
        //目录
        else if(page.getUrl().regex
        		("http(s)?://www\\.meet99\\.com/lvyou").match()) 
        {
        	int i=1;
        	while(page.getHtml().xpath
            		("//ul[@id='treemenu']/li[2]/ul/li["+i+"]")
            		.toString()!=null)
        	{
        		int j=1;
        		while(page.getHtml().xpath
            		("//ul[@id='treemenu']/li[2]/ul/li["+i+"]/ul/li["+j+"]")
            		.toString()!=null)
        		{
        			page.addTargetRequests(page.getHtml().xpath
                    		("//ul[@id='treemenu']/li[2]/ul/li["+i+"]/ul/li["+j+"]/a/@href")
                    		.all());
        			j++;
        		}
        		i++;
        	}
        }
    }

	public static void main(String[] args) 
    {
		HttpClientDownloader httpClientDownloader = new HttpClientDownloader();
        try 
        {
            List<Proxy> proxies = buildProxyIP();
            System.out.println("请求代理IP： " + proxies);
            httpClientDownloader.setProxyProvider(new SimpleProxyProvider(proxies));
        }
        catch (IOException e) 
        {
            e.printStackTrace();
        }
        

    	long startTime, endTime;
        System.out.println("开始爬取数据");
        startTime = System.currentTimeMillis();
        Spider.create(new TravelProcessor())
        	.addUrl("https://www.meet99.com/lvyou")
        	.addPipeline(new MysqlPipeline())
//        	.setDownloader(httpClientDownloader)
                .thread(3).run();
        endTime = System.currentTimeMillis();

        System.err.println("爬取结束，耗时约" + 
        ((endTime - startTime) / 1000) + "秒");
    }
	
	 private static List<Proxy> buildProxyIP() throws IOException 
	 {
	        Document parse = Jsoup.parse(new URL
	        		("http://d.jghttp.golangapi.com/getip?num=50&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=")
	        		, 1000);
	        String pattern = "(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+):(\\d+)";
	        Pattern r = Pattern.compile(pattern);
	        Matcher m = r.matcher(parse.toString());
	        List<Proxy> proxies = new ArrayList<Proxy>();
	        while (m.find()) 
	        {
	            String[] group = m.group().split(":");
	            int prot = Integer.parseInt(group[1]);
	            proxies.add(new Proxy(group[0], prot));
	        }
	        return proxies;
	 }
	 
	 public static void arrange(Page page)
	 {
		 String s = page.getHtml().xpath
         		("//div[@class='type']").toString();
		 String text = "";
//		 System.out.println(s);
		 
		 int a=0,a1=0,a2=0;
		 
		 a = s.indexOf("门票");
		 if(a!=-1)
		 {
			 a1 = s.indexOf("<div>",a);
			 a2 = s.indexOf("</div>",a1+1);
			 text = remove(s.substring(a1+6,a2-2));
			 page.putField("ticket", text);
		 }
		 
		 a = s.indexOf("开放时间",a2);
		 if(a!=-1)
		 {
			 a1 = s.indexOf("<div>",a);
			 a2 = s.indexOf("</div>",a1+1);
			 text = remove(s.substring(a1+6,a2-2));
			 page.putField("opening", text);
		 }
		 
		 a = s.indexOf("交通概况",a2);
		 if(a!=-1)
		 {
			 a1 = s.indexOf("<div>",a);
			 a2 = s.indexOf("</div>",a1+1);
			 text = remove(s.substring(a1+5,a2-2));
			 page.putField("route", text);
		 }
//		 System.out.println(s.substring(a2));
		 a = s.indexOf("简介",a2);
		 if(a!=-1)
		 {
			 a1 = s.indexOf("<p",a);
			 if(a1!=-1)
			 {
				 a2 = s.indexOf("</p>",a1+1);
				 text = remove(s.substring(a1,a2));
//				 System.out.println(s.substring(a1,a2));
				 a1 = s.indexOf("<p",a2);
				 while(a1!=-1)
				 {
					 a2 = s.indexOf("</p>",a1);
					 String text1 = remove(s.substring(a1,a2));
					 if(text1.contains("旅游路线")||text.contains("注意事项"))
					 {
						 a2 = a1;
						 break;
					 }
					 else
					 {
						 text += "\n"+text1;
						 a1 = s.indexOf("<p",a2);
					 }
				 }
			 }
			 else
			 {
				 a1 = s.indexOf("<div>",a);
				 if(a1!=-1)
				 {
					 a2 = s.indexOf("</div>",a1);
					 text = remove(s.substring(a1,a2));
				 }
			 }
			 page.putField("introduction", text);
		 }

		 
		 
		 a = s.indexOf("旅游路线",a2);
		 if(a!=-1)
		 {
			 a1 = s.indexOf("<p>",a);
			 a2 = s.indexOf("</p>",a1+1);
			 text = remove(s.substring(a1+3,a2));
			 page.putField("T_route", text);
		 }
		 
		 a = s.indexOf("注意事项",a2);
		 if(a!=-1)
		 {
			 a1 = s.indexOf("<p>",a);
			 a2 = s.indexOf("</p>",a1+1);
			 text = remove(s.substring(a1+3,a2));
			 page.putField("attention", text);
		 }
	 }
	 
	 public static String remove(String s)
	 {
		 String ss = s.replaceAll("\\u3000", "&nbsp").replaceAll("\n", "")
				 .replaceAll("<strong>[0-9a-zA-Z]</strong>", "").replaceAll("<br>", "br")
				 .replaceAll("<[^>]+>", "").replaceAll("br", "<br>");
				 ;
		 return ss;
	 }
}