package cn.edu.fudan.cs.dstree.util;

import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;
import java.io.*;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

public class TimeSeriesFileUtil {
    public static double[][] readSeriesFromFile(String fileName) throws IOException {
        int timeSeriesCount = (int) getTimeSeriesCount(new File(fileName));
        int timeSeriesLength = getTimeSeriesLength(fileName);
        double[][] ret = new double[timeSeriesCount][timeSeriesLength];

        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        timeSeriesReader.open();
        int i = 0;
        while (timeSeriesReader.hasNext()) {
            double[] next = timeSeriesReader.next();
            ret[i++] = next;
        }
        timeSeriesReader.close();

        return ret;
    }

    public static double[][] readSeriesFromFileAtOnce(String fileName) throws IOException {
        List list = FileUtils.readLines(new File(fileName));
        int count = list.size();
        if (StringUtils.isEmpty(list.get(list.size() - 1).toString()))
            count = count - 1;

        double[] ts = TimeSeriesReader.readFromString(list.get(0).toString());
        double[][] ret = new double[count][ts.length];

        for (int i = 0; i < ret.length; i++) {
            ret[i] = TimeSeriesReader.readFromString(list.get(i).toString());
        }

        return ret;
    }

    public static double[][] readSeriesFromBinaryFileAtOnce(String fileName, int tsLength) throws IOException {
        long fileSize = new File(fileName).length();
        int count = (int) (fileSize / tsLength / 8);
        FileInputStream fis = new FileInputStream(fileName);
        BufferedInputStream bis = new BufferedInputStream(fis);
        DataInputStream dis = new DataInputStream(bis);
        double[][] tss = new double[count][tsLength];

        for (int i = 0; i < count; i++) {
            for (int j = 0; j < tsLength; j++) {
                tss[i][j] = dis.readDouble();
                //            System.out.println("ts[j] = " + ts[j]);
            }
        }

        dis.close();
        bis.close();
        fis.close();
        return tss;
    }

    public static double[][] readSeriesFromFile(String fileName, int[] positions) throws IOException {
        Arrays.sort(positions);
        int tsLength = TimeSeriesFileUtil.getTimeSeriesLength(fileName);
        double[][] ret = new double[positions.length][tsLength];
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        timeSeriesReader.open();
        int c = 0;
        int i = 0;
        while (timeSeriesReader.hasNext()) {
            double[] next = timeSeriesReader.next();
            if (c == positions[i]) {
                ret[i] = next;
                i++;
                if (i >= positions.length)
                    break;
            }
            c++;
        }
        timeSeriesReader.close();

        return ret;
    }

    public static double minDist(double[][] data, double[] queryTs) {
        double minDist = Double.POSITIVE_INFINITY;
        for (int i = 0; i < data.length; i++) {
            double tempDist = DistUtil.euclideanDist(data[i], queryTs);
            if (tempDist < minDist) minDist = tempDist;
        }
        return minDist;
    }


    public static double[] readFromFile(String fileName) throws IOException {
        String s = FileUtils.readFileToString(new File(fileName));
        return readFromString(s);
    }

    public static double[] readFromFile(String fileName, int rows) throws IOException {
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        int tsLength = getTimeSeriesLength(fileName);
        double[] result = new double[rows * tsLength];
        timeSeriesReader.open();
        for (int i = 0; i < rows; i++) {
            timeSeriesReader.hasNext();
            double[] tempTs = timeSeriesReader.next();
            System.arraycopy(tempTs, 0, result, i * tsLength, tsLength);
        }
        timeSeriesReader.close();
        return result;
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

    public static void appendToStream(OutputStream os, double[] timeSeries) throws IOException {
        os.write(timeSeries2Line(timeSeries).getBytes());
    }

    public static int getTimeSeriesLength(String fileName) {
        int ret = 0;
        //read first row
        TimeSeriesReader tsr = new TimeSeriesReader(fileName);
        try {
            tsr.open();
            if (tsr.hasNext()) {
                ret = tsr.next().length;
            }
            tsr.close();
        } catch (IOException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        }
        return ret;
    }

    public static void txtFile2BinFile(String txtFileName, String binFileName) throws IOException {
        FileOutputStream fos = new FileOutputStream(new File(binFileName));
        DataOutputStream dos = new DataOutputStream(new BufferedOutputStream(fos));
        TimeSeriesReader tsr = new TimeSeriesReader(txtFileName);

        tsr.open();
        while (tsr.hasNext()) {
            final double[] ts = tsr.next();
            for (int i = 0; i < ts.length; i++) {
                dos.writeDouble(ts[i]);
            }
        }
        tsr.close();
        dos.close();
    }

    public static NumberFormat formatter = new DecimalFormat("#0.0000");

    public static String timeSeries2Line(double[] timeSeries) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < timeSeries.length; i++) {
            double v = timeSeries[i];
            sb.append(formatter.format(v)).append(" ");
        }
        sb.append("\n");
        return sb.toString();
    }

    public static long getTimeSeriesCount(File fileOrPath) throws IOException {
        long ret = 0;
        if (fileOrPath.exists()) {
            if (fileOrPath.isDirectory()) {
                Collection files = FileUtils.listFiles(fileOrPath, null, false);
                for (Object file : files) {
                    File next = (File) file;
                    ret = ret + getTimeSeriesCount(next);
                }
            } else {
                BufferedReader bfr = new BufferedReader(new FileReader(fileOrPath));
                try {
                    String row = bfr.readLine();
                    while (row != null && row.trim().length() > 0) {
                        ret++;
                        row = bfr.readLine();
                    }
                } finally {
                    bfr.close();
                }
            }
        }
        return ret;
    }
}
