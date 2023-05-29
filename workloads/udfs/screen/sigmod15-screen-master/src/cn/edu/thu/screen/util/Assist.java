package cn.edu.thu.screen.util;

import cn.edu.thu.screen.entity.TimePoint;
import cn.edu.thu.screen.entity.TimeSeries;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class Assist {
  public static String PATH = "data/";

  /**
   * Basic attributes: timestamp, dirty, truth
   *
   * @param filename filename
   * @param index which column besides timestamp should be read
   * @param splitOp to split up the rows
   * @return data in timeseries form
   */
  public TimeSeries readData(String filename, int index, String splitOp) {
    TimeSeries timeSeries = new TimeSeries();

    try {
      FileReader fr = new FileReader(PATH + filename);
      BufferedReader br = new BufferedReader(fr);

      String row;
      long timestamp;
      double value;
      TimePoint tp;

      while ((row = br.readLine()) != null) {
        String[] vals = row.split(splitOp);
        timestamp = Long.parseLong(vals[0]);
        value = Double.parseDouble(vals[index]);

        tp = new TimePoint(timestamp, value);
        timeSeries.addTimePoint(tp);
      }

      br.close();
      fr.close();
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }

    return timeSeries;
  }

  /**
   * RMS sqrt(|modify - truth|^2 / len)
   *
   * @param truthSeries truth
   * @param resultSeries after repair
   * @return RMS error
   */
  public double calcRMS(TimeSeries truthSeries, TimeSeries resultSeries) {
    double cost = 0;
    double delta;
    int len = truthSeries.getLength();

    for (int i = 0; i < len; ++i) {
      delta = resultSeries.getTimeseries().get(i).getModify()
          - truthSeries.getTimeseries().get(i).getValue();

      cost += delta * delta;
    }
    cost /= len;

    return Math.sqrt(cost);
  }

}
