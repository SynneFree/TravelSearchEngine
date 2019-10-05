package org.group01.travel;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.remote.DesiredCapabilities;

import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.ResultItems;
import us.codecraft.webmagic.Task;
import us.codecraft.webmagic.pipeline.Pipeline;

public class MysqlPipeline implements Pipeline
{
	public MysqlPipeline() 
	{
    }

	@Override    
	public void process(ResultItems resultItems, Task task) 
	{        
		Connection con = database.getConnection();
		PreparedStatement ptmt = null;
		ResultSet rs = null;
		
		String name = resultItems.get("name"); 
		String introduction = resultItems.get("introduction");
		String distribution = resultItems.get("distribution");
		String rank = resultItems.get("rank");
		String strategy = resultItems.get("strategy");
		String route = resultItems.get("route");
		String ticket = resultItems.get("ticket");
		String opening = resultItems.get("opening");
		String service = resultItems.get("service");
		String feature = resultItems.get("feature");
		String position = resultItems.get("position");
		String official = resultItems.get("official");
		String phone = resultItems.get("phone");
		String attention = resultItems.get("attention");
		String T_route = resultItems.get("T_route");
		String BestTime = resultItems.get("BestTime");
		String shopping = resultItems.get("shopping");
		String around = resultItems.get("around");
		String map = resultItems.get("map");
		String picture = resultItems.get("picture");
		
		if(name==null)
		{
			return;
		}
		else 
		{
			String search = "select * from spot_99 where name=?";
			try 
			{
				ptmt = con.prepareStatement(search);
				ptmt.setString(1, name);
				rs = ptmt.executeQuery();
				if(rs.next())
				{
					System.out.println(name+"已存在");
					return;
				}
			} 
			catch (SQLException e) 
			{
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
		
		String sql = "insert into spot_99 "
				+ "(name, introduction, distribution, rank, strategy, route, ticket, "
				+ "opening, service, feature, position, official, phone, attention, "
				+ "T_route, BestTime, shopping, around, map, picture)"
				+ " values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)";        
		try 
		{            
			ptmt = con.prepareStatement(sql);  
			
			ptmt.setString(1,name);
			
			//简介
			if(introduction!=null&&introduction.length()>2000)
			{
				ptmt.setString(2,introduction.substring(0, 2000)); 
			}
			else
			{
				ptmt.setString(2,introduction); 
			}
			
			//分布
			if(distribution!=null&&distribution.length()>2000)
			{
				ptmt.setString(3,distribution.substring(0, 2000)); 
			}
			else
			{
				ptmt.setString(3,distribution); 
			}
			
			//资质
			if(rank!=null&&rank.length()>1000)
			{
				ptmt.setString(4,rank.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(4,rank); 
			}
			
			//攻略
			if(strategy!=null&&strategy.length()>2000)
			{
				ptmt.setString(5,strategy.substring(0, 2000)); 
			}
			else
			{
				ptmt.setString(5,strategy); 
			}
			
			//路线
			if(route!=null&&route.length()>2000)
			{
				ptmt.setString(6,route.substring(0, 2000)); 
			}
			else
			{
				ptmt.setString(6,route); 
			}
			
			//门票
			if(ticket!=null&&ticket.length()>1000)
			{
				ptmt.setString(7,ticket.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(7,ticket); 
			}
			
			//开放
			if(opening!=null&&opening.length()>1000)
			{
				ptmt.setString(8,opening.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(8,opening); 
			}
			
			//服务
			if(service!=null&&service.length()>1000)
			{
				ptmt.setString(9,service.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(9,service); 
			}
			
			//特色
			if(feature!=null&&feature.length()>1000)
			{
				ptmt.setString(10,feature.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(10,feature); 
			}
			
			//位置
			if(position!=null&&position.length()>100)
			{
				ptmt.setString(11,position.substring(0, 100)); 
			}
			else
			{
				ptmt.setString(11,position); 
			}
			
			//官网
			if(official!=null&&official.length()>100)
			{
				ptmt.setString(12,official.substring(0, 100)); 
			}
			else
			{
				ptmt.setString(12,official); 
			}
			
			//电话
			if(phone!=null&&phone.length()>100)
			{
				ptmt.setString(13,phone.substring(0, 100)); 
			}
			else
			{
				ptmt.setString(13,phone); 
			}
			
			//注意
			if(attention!=null&&attention.length()>1000)
			{
				ptmt.setString(14,attention.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(14,attention); 
			}
			
			//旅游路线
			if(T_route!=null&&T_route.length()>2000)
			{
				ptmt.setString(15,T_route.substring(0, 2000)); 
			}
			else
			{
				ptmt.setString(15,T_route); 
			}
			
			//最佳
			if(BestTime!=null&&BestTime.length()>1000)
			{
				ptmt.setString(16,BestTime.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(16,BestTime); 
			}
			
			//购物
			if(shopping!=null&&shopping.length()>1000)
			{
				ptmt.setString(17,shopping.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(17,shopping); 
			}
			
			//周边
			if(around!=null&&around.length()>1000)
			{
				ptmt.setString(18,around.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(18,around); 
			}
			
			//地图
			if(map!=null&&map.length()>100)
			{
				ptmt.setString(19,map.substring(0, 100)); 
			}
			else
			{
				ptmt.setString(19,map); 
			}
			
			//图片
			if(picture!=null&&picture.length()>1000)
			{
				ptmt.setString(20,picture.substring(0, 1000)); 
			}
			else
			{
				ptmt.setString(20,picture); 
			}
			
			ptmt.execute();        
		} 
		catch (SQLException e) 
		{            
			e.printStackTrace();        
		} 	
	}
	
	public static void updatePicture(Page page, int n)
	{
		//取名字
		String s = page.getHtml().xpath("//div[@id='jdleft']/h1/text()").toString();
		int a = s.indexOf("旅游攻略");
		if(a==-1)
    	{
    		a = s.indexOf("校园风光");
    	}
		String name = s.substring(0,a);
		if(name==null)
		{
			System.out.println("no name");
			return;
		}
		
		Connection con = database.getConnection();
		PreparedStatement ptmt = null;
		ResultSet rs = null;
		
		//取图片
		String picture = "";
		String sql = "select * from spot_99 where name=?";
		try 
		{
			ptmt = con.prepareStatement(sql);
			ptmt.setString(1, name);
			rs = ptmt.executeQuery();
			if(rs.next())
			{
				picture += rs.getString("picture");
			}
		} 
		catch (SQLException e1) 
		{
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		int len1 = picture.length();
		int len2 = picture.replaceAll(";", "").length();
		int num = len1-len2;
		if(n<=num)
		{
			System.out.println(n+"已存在");
			return;
		}
		
		DesiredCapabilities sCaps = new DesiredCapabilities();
		sCaps.setJavascriptEnabled(true);
		System.getProperties().setProperty
        ("webdriver.chrome.driver", "D:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe");
		WebDriver w = new ChromeDriver(sCaps);
		
		w.get(page.getUrl().toString());
		
		if(!Pspot_99.refresh(w,page,"//div[@id='curphoto']/div"))
		{
			w.quit();
			return;
		}
		
		WebElement e = w.findElement(By.xpath("//div[@id='curphoto']/div"));	
        s = e.getAttribute("outerHTML");
        int a2 = s.indexOf(".jpg");
        int a1 = s.lastIndexOf("https:", a2);
        String link = s.substring(a1, a2+4);
        
        String p = s.substring(s.lastIndexOf("/", a2)+1,a2+4);
        if(picture.contains(p))
        {
        	w.quit();
        	return;
        }
        Pspot_99.downloadPicture(link, p);
        
		
		sql = "update spot_99 set picture=? where name=?";
		try 
		{
			ptmt = con.prepareStatement(sql);
			ptmt.setString(1, picture+p+";");
			ptmt.setString(2, name);
			ptmt.execute();
		} 
		catch (SQLException e1) 
		{
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}  
		
		w.quit();
	}
	
	public static Boolean nameExist(String name)
	{
		Connection con = database.getConnection();
		PreparedStatement ptmt = null;
		ResultSet rs = null;
		
		String search = "select * from spot_99 where name=?";
		try 
		{
			ptmt = con.prepareStatement(search);
			ptmt.setString(1, name);
			rs = ptmt.executeQuery();
			if(rs.next())
			{
				System.out.println(name+"已存在");
				return true;
			}
		} 
		catch (SQLException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return false;
	}
}
