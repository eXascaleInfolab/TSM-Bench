package cn.edu.thu.screen;

import cn.edu.thu.screen.entity.TimePoint;
import cn.edu.thu.screen.entity.TimeSeries;
import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by Stoke on 2017/10/7.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class Screen {

  private TimeSeries timeseries;
  private TimePoint kp;

  private long T;       // the window size
  private double SMAX;  // maximum speed
  private double SMIN;  // minimum speed

  /**
   *
   * @param timeseries timeseries
   * @param sMax maximum allowed speed
   * @param sMin minimum allowed speed
   * @param t the window size
   */
  public Screen(TimeSeries timeseries, double sMax, double sMin, long t) {
    setTimeSeries(timeseries);
    setT(t);
    setSMAX(sMax);
    setSMIN(sMin);
  }

  public void setTimeSeries(TimeSeries timeSeries) {
    this.timeseries = timeSeries;
  }

  public void setT(long t) {
    T = t;
  }

  public void setSMAX(double SMAX) {
    this.SMAX = SMAX;
  }

  public void setSMIN(double SMIN) {
    this.SMIN = SMIN;
  }

  /**
   *
   * @return timeseries after repair
   */
  public TimeSeries mainScreen() {
    ArrayList<TimePoint> totalList = timeseries.getTimeseries();
    int size = totalList.size();

    long preEnd = -1, curEnd;
    // the startTime in the window, the real end time in the window, the maximum allowed
    long wStartTime, wEndTime, wGoalTime;
    long curTime;
    TimePoint prePoint = null;    // the last fixed point
    TimePoint tp;

    TimeSeries tempSeries = new TimeSeries();
    ArrayList<TimePoint> tempList;

    int readIndex = 1; // the point should be read in

    // initial
    tp = totalList.get(0);
    tempSeries.addTimePoint(tp);
    wStartTime = tp.getTimestamp();
    wEndTime = wStartTime;
    wGoalTime = wStartTime + T;

    while (readIndex < size) {
      tp = totalList.get(readIndex);
      curTime = tp.getTimestamp();

      // This point shouldn't be added until the repair is over
      if (curTime > wGoalTime) {
        while (true) {
          tempList = tempSeries.getTimeseries();
          if (tempList.size() == 0) {
            // if all the points in tempList has been handled
            tempSeries.addTimePoint(tp);  // the current point should be a new start
            wGoalTime = curTime + T;
            wEndTime = curTime;
            break;
          }

          kp = tempList.get(0);
          wStartTime = kp.getTimestamp();
          wGoalTime = wStartTime + T;

          if (curTime <= wGoalTime) {
            // then should read in new points
            tempSeries.addTimePoint(tp);
            wEndTime = curTime;
            break;
          }

          curEnd = wEndTime;

          if (preEnd == -1) {
            prePoint = kp;
          }

          local(tempSeries, prePoint);

          prePoint = kp;
          prePoint.setModified(true);
          preEnd = curEnd;

          // remove the keyPoint
          tempSeries.getTimeseries().remove(0);
        } // end of while(true)
      } else {
        if (curTime > wEndTime) {
          // suppose the sequence is in order, so it must happen
          tempSeries.addTimePoint(tp);
          wEndTime = curTime;
        }
      }

      readIndex++;  // read another one
    }
    // form resultSeries
    TimeSeries resultSeries = new TimeSeries();
    long timestamp;
    double modify;

    for (TimePoint timePoint : timeseries.getTimeseries()) {
      timestamp = timePoint.getTimestamp();
      modify = timePoint.getModify();
      tp = new TimePoint(timestamp, modify);
      resultSeries.addTimePoint(tp);
    }

    return resultSeries;
  }

  /**
   * Algorithm 1
   *
   * @param timeSeries timeseries in a window
   * @param prePoint the former modified point
   */
  private void local(TimeSeries timeSeries, TimePoint prePoint) {
    ArrayList<TimePoint> tempList = timeSeries.getTimeseries();
    // get bound
    long preTime = prePoint.getTimestamp();
    double preVal = prePoint.getModify();
    long kpTime = kp.getTimestamp();

    double lowerBound = preVal + SMIN * (kpTime - preTime);
    double upperBound = preVal + SMAX * (kpTime - preTime);

    // form candidates
    ArrayList<Double> xkList = new ArrayList<>();
    int len = tempList.size();

    xkList.add(kp.getModify());

    TimePoint tp;
    for (int i = 1; i < len; ++i) {
      tp = tempList.get(i);
      double val = tp.getModify();
      long dTime = kpTime - tp.getTimestamp();
      xkList.add(val + SMIN * dTime);
      xkList.add(val + SMAX * dTime);
    }

    Collections.sort(xkList);
    double xMid = xkList.get(len - 1);
    double modify = xMid;
    if (upperBound < xMid) {
      modify = upperBound;
    } else if (lowerBound > xMid) {
      modify = lowerBound;
    }

    kp.setModify(modify);
  }
}

