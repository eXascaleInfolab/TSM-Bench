package cn.edu.fudan.cs.dstree.util;

import java.io.*;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 10-12-30
 * Time: 下午3:17
 * To change this template use File | Settings | File Templates.
 */
public class TimeSeriesReader {
    BufferedReader bfr;
    String fileName;

    public String getFileName() {
        return fileName;
    }

    public TimeSeriesReader(String fileName) {
        this.fileName = fileName;
    }

    String row;

    public boolean hasNext() throws IOException {
        row = bfr.readLine();
        return (row != null && row.trim().length() > 0);
    }

    static String SEPARATOR = " |\t|\n";

    public static double[] readFromString(String str) {
        String[] strings = str.split(SEPARATOR);

        double[] ret = new double[strings.length];

        for (int i = 0; i < ret.length; i++) {
            String s = strings[i];
            if (s.length() > 0)
                ret[i] = Double.parseDouble(s);
        }
        return ret;
    }

    public double[] next() {
        return readFromString(row);
    }

    public void open() throws FileNotFoundException {
        bfr = new BufferedReader(new FileReader(new File(fileName)));
    }

    public void close() throws IOException {
        bfr.close();
    }
}
