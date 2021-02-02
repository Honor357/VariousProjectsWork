/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package grafana_screener;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.ParseException;
import java.time.LocalDateTime;
import javax.imageio.ImageIO;
import java.io.BufferedReader;
import java.text.SimpleDateFormat;
import java.util.Date;



/**
 *
 * @author Honor
 */
public class Grafana_Screener {

    /**
     * @param args the command line arguments
     */
     public static void main(String[] args) throws MalformedURLException, IOException, ParseException {
        saveimg("http://www.avajava.com/images/avajavalogo.jpg","downloaded.jpg");
        readerfile();
        LocalDateTime currentDateTime = LocalDateTime.now();
        GenerateUrl("2021-01-26 13:18:38","2021-01-29 17:18:38");
    }
    
    public static void saveimg (String Url_img, String path) throws MalformedURLException, IOException {
        URL url = new URL(Url_img);
        BufferedImage img = ImageIO.read(url);
        File file = new File(path);
        ImageIO.write(img, "jpg", file);
    }
    
     public static void readerfile() throws FileNotFoundException, IOException {
       try {
            File file = new File("test.txt");
            FileReader fr = new FileReader(file);
            BufferedReader reader = new BufferedReader(fr);
            String line = reader.readLine();
            while (line != null) {
                System.out.println(line);
                ParceUrl(line);
                line = reader.readLine();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }    
     }
     
     public static void ParceUrl(String url) throws FileNotFoundException, IOException {
       String result = url.substring(url.indexOf("from=")+5,url.indexOf("&to=")); // TODO code application logic here
       System.out.println(result);
       String result1 = url.substring(url.indexOf("&to=")+4,url.indexOf("&panelId")); // TODO code application logic here
       System.out.println(result1);
     }
     
    public static String ConvertTimeToTimeStamp(String date1) throws ParseException  {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = sdf.parse(date1);
        String  unixTime = Long.toString((date.getTime() / 1000L)+18000)+"000";
        System.out.println(unixTime);
        return unixTime;
     }
 
    public static void GenerateUrl(String dateStart, String dateEnd) throws ParseException  {
        String url = "http://eosmonitoring:3000/render/d-solo/iMowdtHZz/marathon-docker-dashboard?orgId=1&refresh=30s&var-Host="
                + "u1ufrmcrmlt1.moscow.alfaintra.net&var-Host=u1ufrstmtlt1.moscow.alfaintra.net&var-Host=u1ufrufncinslt1.moscow.alfaintra.net&var-Host=u2ufrmcrmlt1.moscow.alfaintra.net&var-Host=u2ufrstmtlt1.moscow.alfaintra.net&var-Host=u2ufrufncinslt1.moscow.alfaintra.net&var-Host=u3ufrmcrmlt1.moscow.alfaintra.net&var-Host=u4ufrmcrmlt1.moscow.alfaintra.net&var-Docker_Stack=All&var-image=docker.moscow.alfaintra.net%2Fmarathon-lb&var-container_name=kafka_manager&"
                + "from=" + ConvertTimeToTimeStamp(dateStart)  
                + "&to=" + ConvertTimeToTimeStamp(dateEnd) 
                + "&panelId=4&"
                + "width=1500&"
                + "height=800&"
                + "tz=Asia%2FYekaterinburg";

        System.out.println(url);
     }
     
}
    

