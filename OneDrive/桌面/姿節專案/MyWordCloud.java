import com.kennycason.kumo.CollisionMode;
import com.kennycason.kumo.WordCloud;
import com.kennycason.kumo.WordFrequency;
import com.kennycason.kumo.bg.CircleBackground;
import com.kennycason.kumo.font.KumoFont;
import com.kennycason.kumo.font.scale.LinearFontScalar;
import com.kennycason.kumo.palette.ColorPalette;

import java.awt.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class MyWordCloud {

    // 資料庫資訊
    static String url = "jdbc:mysql://127.0.0.16/word";
	static String username = "root";
	static String password = "root";

    // 產生的文字雲png輸出位置
    static String outputPath = "./wordcloud.png";

    /* mySql指令

    create database `word`;
    create table `count_word`(
	    `word` varchar(20),
        `frequency` INT
    );

    insert into `count_word` values ('特斯拉', 9);  特斯拉出現9次
    
    */

    public static void main(String[] args) {

        try (Connection connection = DriverManager.getConnection(url, username, password)) {

            List<WordFrequency> wordFrequencies = getDataFromDatabase(connection);
            generateWordCloud(wordFrequencies);

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private static List<WordFrequency> getDataFromDatabase(Connection connection) throws SQLException {
        List<WordFrequency> wordFrequencies = new ArrayList<>();

        String query = "SELECT word, frequency FROM count_word";
        try (Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery(query)) {

            while (resultSet.next()) {
                
                String word = resultSet.getString("word");
                int frequency = resultSet.getInt("frequency");

                wordFrequencies.add(new WordFrequency(word, frequency));
            }
        }

        return wordFrequencies;
    }

    private static void generateWordCloud(List<WordFrequency> wordFrequencies) {

        Dimension dimension = new Dimension(600, 600);
        WordCloud wordCloud = new WordCloud(dimension, CollisionMode.PIXEL_PERFECT);
        wordCloud.setPadding(2);
        wordCloud.setBackground(new CircleBackground(300));
        wordCloud.setColorPalette(new ColorPalette(new Color(0x4055F1), new Color(0x408DF1), new Color(0x40AAF1)));
        wordCloud.setFontScalar(new LinearFontScalar(10, 40));
        wordCloud.setKumoFont(new KumoFont(new Font("SimSun", Font.PLAIN, 1)));
        wordCloud.build(wordFrequencies);

        try {
            wordCloud.writeToFile(outputPath);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
