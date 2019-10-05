package org.group01.travel;


import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.DesiredCapabilities;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

import org.apache.commons.exec.*;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.selector.Html;

public class Pspot_99 
{
	public static void process(Page page)
	{
		String s = page.getHtml().xpath("//div[@id='jdleft']/h1/text()").toString();
		int a1=0,a2=0;
		//景区名称
    	int a = s.indexOf("旅游攻略");
    	if(a==-1)
    	{
    		a = s.indexOf("校园风光");
    	}
    	if(MysqlPipeline.nameExist(s.substring(0,a)))
    	{
    		return;
    	}
        page.putField("name", s.substring(0,a));
        System.out.println(page.getResultItems().get("name"));
        
        DesiredCapabilities sCaps = new DesiredCapabilities();
		sCaps.setJavascriptEnabled(true);
		System.getProperties().setProperty
        ("webdriver.chrome.driver", "D:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe");
		WebDriver w = new ChromeDriver(sCaps);

		w.get(page.getUrl().toString());
		if(!refresh(w,page,"//div[@id='curphoto']/div"))
		{
			w.quit();
			return;
		}
        
        int j = 1;
        int i = 1;
        while(page.getHtml().xpath
        		("//div[@class='hd']/ul/li["+j+"]")
        		.toString()!=null)
        {
        	i=1;
        	a1 = a2 = 0;
        	if(page.getHtml().xpath
            		("//div[@class='hd']/ul/li["+j+"]")
            		.toString().contains("学校介绍")||
            		page.getHtml().xpath
            		("//div[@class='hd']/ul/li["+j+"]")
            		.toString().contains("景区介绍"))
        	{
        		//简介、分布、资质、特色
                s = page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]")
                		.toString();
                while(page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]/h2["+i+"]")
                		.toString()!=null)
                {
                	a1 = s.indexOf("</h2>",a2);
            		a2 = s.indexOf("<h2>", a1);
            		if(a2==-1)
            		{
            			a2 = s.indexOf("<div",a1);
            			if(a2==-1)
            			{
            				a2 = s.indexOf("</div",a1);
            			}
            		}
                	if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区简介")||
                    		page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("学校简介"))
                	{
                		page.putField("introduction", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景点分布")||
                    		page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("地点分布"))
                	{
                		page.putField("distribution", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区资质"))
                	{
                		page.putField("rank", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区特色")||
                    		page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("学校特色"))
                	{
                		page.putField("feature", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区游览图"))
                	{
                		WebElement e = w.findElement(By.xpath("/html"));
                		e.sendKeys(Keys.END);
                		try {
							Thread.sleep(1000);
						} catch (InterruptedException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
                		if(!refresh2(w,page,"//div[@class='bd']/div["+j+"]//div[@class='img']"))
                		{
                			w.quit();
                			return;
                		}
                		e = w.findElement(By.xpath("//div[@class='bd']/div["+j+"]//div[@class='img']"));
                        s = e.getAttribute("outerHTML");
                        a1 = s.indexOf("https:");
                        a2 = s.indexOf(".jpg",a1);
                        
                        String link = s.substring(a1, a2+4);
                        downloadPicture(link, s.substring(s.lastIndexOf("/", a2)+1,a2+4));
                		page.putField("map", s.substring(s.lastIndexOf("/", a2)+1, a2+4));
                	}
                	i++;
                }
        	}
        	else if(page.getHtml().xpath
            		("//div[@class='hd']/ul/li["+j+"]")
            		.toString().contains("旅游攻略"))
        	{
        		 //最佳时间、购物推荐、旅游攻略、游览路线
                s = page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]")
                		.toString();
                while(page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]/h2["+i+"]")
                		.toString()!=null)
                {
                	a1 = s.indexOf("</h2>",a2);
            		a2 = s.indexOf("<h2>", a1);
            		if(a2==-1)
            		{
            			a2 = s.indexOf("<div",a1);
            			if(a2==-1)
            			{
            				a2 = s.indexOf("</div",a1);
            			}
            		}
                	if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("最佳游览时间"))
                	{
                		page.putField("BestTime", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if
                	(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("购物推荐"))
                	{
                		page.putField("shopping", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if
                	(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("旅游攻略"))
                	{
                		page.putField("strategy", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if
                	(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("游览路线"))
                	{
                		page.putField("T_route", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	i++;
                }
        	}
        	else if(page.getHtml().xpath
            		("//div[@class='hd']/ul/li["+j+"]")
            		.toString().contains("怎么去"))
        	{
        		//位置、路线
                s = page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]")
                		.toString();
                while(page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]/h2["+i+"]")
                		.toString()!=null)
                {
                	a1 = s.indexOf("</h2>",a2);
            		a2 = s.indexOf("<h2>", a1);
            		if(a2==-1)
            		{
            			a2 = s.indexOf("<div",a1);
            			if(a2==-1)
            			{
            				a2 = s.indexOf("</div",a1);
            			}
            		}
                	if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区位置")||
                    		page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("学校位置"))
                	{
                		page.putField("position", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("到达方式"))
                	{
                		page.putField("route", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	i++;
                }
        	}
        	else if(page.getHtml().xpath
            		("//div[@class='hd']/ul/li["+j+"]")
            		.toString().contains("门票"))
        	{
        		//门票、开放
                s = page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]")
                		.toString();
                while(page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]/h2["+i+"]")
                		.toString()!=null)
                {
                	a1 = s.indexOf("</h2>",a2);
            		a2 = s.indexOf("<h2>", a1);
            		if(a2==-1)
            		{
            			a2 = s.indexOf("<div",a1);
            			if(a2==-1)
            			{
            				a2 = s.indexOf("</div",a1);
            			}
            		}
                	if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("门票价格"))
                	{
                		page.putField("ticket", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("开放时间"))
                	{
                		page.putField("opening", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	i++;
                }
        	}
        	else if(page.getHtml().xpath
            		("//div[@class='hd']/ul/li["+j+"]")
            		.toString().contains("服务"))
        	{
        		//官网、服务、电话、注意事项
        		s = page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]")
                		.toString();
                while(page.getHtml().xpath
                		("//div[@class='bd']/div["+j+"]/h2["+i+"]")
                		.toString()!=null)
                {
                	a1 = s.indexOf("</h2>",a2);
            		a2 = s.indexOf("<h2>", a1);
            		if(a2==-1)
            		{
            			a2 = s.indexOf("<div",a1);
            			if(a2==-1)
            			{
            				a2 = s.indexOf("</div",a1);
            			}
            		}
                	if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区官网")||
                    		page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("学校网站"))
                	{
                		page.putField("official", page.getHtml().xpath
                        		("//div[@class='bd']/div["+j+"]/a/@href")
                        		.toString());
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区服务"))
                	{
                		page.putField("service", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("景区电话")||
                    		page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("学校电话"))
                	{
                		page.putField("phone", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	else if(page.getHtml().xpath
                    		("//div[@class='bd']/div["+j+"]/h2["+i+"]/text()")
                    		.toString().contains("注意事项"))
                	{
                		page.putField("attention", TravelProcessor.remove(s.substring(a1+5,a2)));
                	}
                	i++;
                }
        	}
        j++;
        }
        
        //周边景点
        i=1;
        String ar = "";
        while(page.getHtml().xpath
        		("//div[@class='zone']/div/a["+i+"]").toString()!=null)
        {
        	ar += page.getHtml().xpath
            		("//div[@class='zone']/div/a["+i+"]/text()").toString()
            		+";";
        	i++;
        }
        page.putField("around", TravelProcessor.remove(ar)); 
        
        //图片
        WebElement e = w.findElement(By.xpath("//div[@id='curphoto']/div"));	
        s = e.getAttribute("outerHTML");
        a2 = s.indexOf(".jpg");
        a1 = s.lastIndexOf("https:", a2);
        String link = s.substring(a1, a2+4);
        downloadPicture(link, s.substring(s.lastIndexOf("/", a2)+1,a2+4));
		page.putField("picture", s.substring(s.lastIndexOf("/", a2)+1, a2+4)+";");
		
		w.quit();
        
	}
	
	public static void downloadPicture(String u, String map)
	{
		String dir = "D:\\过去的学习\\图片\\";
		try 
		{
			URL url = new URL(u);
			try 
			{
				DataInputStream dataInputStream = new DataInputStream(url.openStream());
				FileOutputStream fileOutputStream = new FileOutputStream(new File(dir + map));
				byte[] buffer = new byte[1024 * 50];
				int length;
				while ((length = dataInputStream.read(buffer)) > 0) 
				{
	                fileOutputStream.write(buffer, 0, length);
	            }
				System.out.println("已经下载：" + dir + map);
				dataInputStream.close();
				fileOutputStream.close();
			} 
			catch (IOException e) 
			{
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} 
		catch (MalformedURLException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static boolean refresh(WebDriver w, Page page, String path)
	{
		int count = 0;
		WebElement test = w.findElement(By.xpath(path));
		String s = test.getAttribute("outerHTML");
		
		while((s.indexOf(".jpg")==-1)&&count<20)
		{
			w.get(page.getUrl().toString());
			try {
				Thread.sleep(3000);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			test = w.findElement(By.xpath(path));
			s = test.getAttribute("outerHTML");
			count++;
		}
		if(count>=20)
		{
			return false;
		}
		else
		{
			return true;
		}
	}
	
	public static boolean refresh2(WebDriver w, Page page, String path)
	{
		int count = 0;
		WebElement test = w.findElement(By.xpath(path));
		String s = test.getAttribute("outerHTML");
		
		while((s.indexOf(".jpg")==-1)&&count<20)
		{
			w.get(page.getUrl().toString());
			try {
				Thread.sleep(3000);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			WebElement e = w.findElement(By.xpath("/html"));
    		e.sendKeys(Keys.END);
    		try {
				Thread.sleep(1000);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			test = w.findElement(By.xpath(path));
			s = test.getAttribute("outerHTML");
			count++;
		}
		if(count>=20)
		{
			return false;
		}
		else
		{
			return true;
		}
	}
}
