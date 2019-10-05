package org.group01.travel;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class database 
{
	private static final String URL
		="jdbc:mysql://localhost:3306/travel?serverTimezone=GMT%2B8";    
	private static final String USER="root";    
	private static final String PASSWORD="123456";
	private static Connection con = null;
	static
	{
		try 
		{
			Class.forName("com.mysql.cj.jdbc.Driver");//得到DriverManager，在下面建立连接时使用
		} 
		catch(ClassNotFoundException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public static Connection getConnection()
	{
		try 
		{
			con = DriverManager.getConnection(URL,USER,PASSWORD);
		} 
		catch (SQLException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        return con;
    }
}
