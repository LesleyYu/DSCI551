import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class SQL2MR {

    public static class TokenizerMapper extends Mapper<LongWritable, Text, Text, FloatWritable> {
        private Text outputKey = new Text();
        private FloatWritable outputValue = new FloatWritable();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] fields = value.toString().split(",");
            if (fields.length == 12) {
                int length = Integer.parseInt(fields[8]);
                if (length >= 60) {
                    String rating = fields[10];
                    float replacementCost = Float.parseFloat(fields[9]);
                    outputKey.set(rating);
                    outputValue.set(replacementCost);
                    context.write(outputKey, outputValue);
                }
            }
        }
    }

  public static class FloatAvgReducer 
       extends Reducer<Text,FloatWritable,Text,FloatWritable> {
    private FloatWritable result = new FloatWritable();

    public void reduce(Text key, Iterable<FloatWritable> values, Context context
              ) throws IOException, InterruptedException {
      int count = 0;
      float sum = 0;
      for (FloatWritable val : values) {
          sum += val.get();
          count++;
      }
      if (count >= 160) {
          float average = sum / count;
          result.set(average);
          context.write(key, result);
      }
     
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
    if (otherArgs.length < 2) {
      System.err.println("Usage: sql2mr <in> [<in>...] <out>");
      System.exit(2);
    }
    Job job = Job.getInstance(conf, "word count");
    job.setJarByClass(SQL2MR.class);

    job.setMapperClass(TokenizerMapper.class);
    job.setReducerClass(FloatAvgReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(FloatWritable.class);
    
    for (int i = 0; i < otherArgs.length - 1; ++i) {
      FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
    }
    FileOutputFormat.setOutputPath(job,
      new Path(otherArgs[otherArgs.length - 1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}