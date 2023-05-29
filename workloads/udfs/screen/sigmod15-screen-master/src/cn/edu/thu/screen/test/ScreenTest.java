package cn.edu.thu.screen.test;

import cn.edu.thu.screen.Screen;
import cn.edu.thu.screen.entity.TimeSeries;
import cn.edu.thu.screen.util.Assist;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class ScreenTest {

  public static void main(String[] args) {
    String inputFileName = "stock10k.data";

    Assist assist = new Assist();
    String splitOp = ",";

    TimeSeries dirtySeries = assist.readData(inputFileName, 1, splitOp);
    TimeSeries truthSeries = assist.readData(inputFileName, 2, splitOp);

    double rmsDirty = assist.calcRMS(truthSeries, dirtySeries);
    System.out.println("Dirty RMS error is " + rmsDirty);

    double sMax = 6;
    double sMin = -6;
    long T = 1;
    Screen screen = new Screen(dirtySeries, sMax, sMin, T);
    TimeSeries resultSeries = screen.mainScreen();

    double rms = assist.calcRMS(truthSeries, resultSeries);

    System.out.println("Repair RMS error is " + rms);
  }
}
