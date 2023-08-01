use strict;
use warnings;
use SVG;
####Copied colour palette for chromosomes.
my %chr_col;

##Image Size X for width, Y for Height##
my $X=shift;
$X=int($X+100);
my $Y=$X;
my $sqrt2=sqrt(2);
## Size of margins
my $y_top_margin=10;
my $y_bottom_margin=10;
my $x_left_margin=10;
my $x_right_margin=10;

## Shape related parameters
my $interval=350;
my $gen_tick_len=50;
my $chr_tick_len=50;
my $axis_tick=10;
my $axis_tick_sp=5;
my $chr_wid=10;



###Loading information of length of chromosomes from a file, useful when you have multiple chromosomes/scaffolds to work with 
my %xlen;
my %ylen;
my %source;

#Input lastz
my $file_in=shift;

#set up start(minimal) and end (maximal) position
my $x_chr_start=shift;
my $x_chr_end=shift;
$x_chr_end=int($x_chr_end+1000);
#default square plot x-axis = y-axis#

my $y_chr_start=$x_chr_start;
my $y_chr_end=$x_chr_end;

###Declaim the SVG
my $outname=shift;
my $bin_size=shift;

my $svg=SVG->new(width=>$X,height=>$Y);
my $box_h=$Y-$y_top_margin-$y_bottom_margin;
my $box_w=$X-$x_left_margin-$x_right_margin;

$svg->rect(x=>$x_left_margin,y=>$y_bottom_margin, width=>$box_w,height=>$box_h,
           rx    => 0, ry     =>0,
		   style=>{'stroke'=>'gray','opacity'=>'0.5','fill'=>'white',
		   'stroke-width'=>'0.5'}
		   );


my $total_x_chr=$x_chr_end-$x_chr_start;
my $total_y_chr=$y_chr_end-$y_chr_start;
my $Xpx_per_kb=($box_w/$total_x_chr)*1000;
my $Ypx_per_kb=($box_h/$total_y_chr)*1000;
print "Totoalx:$total_x_chr\tX-BPP:$Xpx_per_kb per kb\n";
print "Totoaly:$total_y_chr\tY-BPP:$Ypx_per_kb per kb\n";

if ($file_in =~ /.gz$/) {
   open(LZH1, "gunzip -c $file_in |") || die $!;
}else {
   open(LZH1, $file_in) ||die $!;
}

my $chr1="";
while(<LZH1>){
	chomp;
	next if($_=~/^#/);
	my ($name1,$start1,$end1,$length1,$name2,$strand2,$length2,$start2,$end2,$cgap,$identity,$idPct,$score)=split(/\s+/,$_);
	$chr1=$name1;
	$idPct=substr($idPct,0,-1);
	#next if($idPct<91);
	next if($name1=~/^scaf/);
	next if($end1<$x_chr_start||$start1>$x_chr_end||$end2<$y_chr_start||$start2>$y_chr_end);
	if($start1==1 && $end1-$start1>10000000){
		$start1=$x_chr_start;
		$end1=$x_chr_end;
		$start2=$y_chr_start;
		$end2=$y_chr_end;
	}
	if($length2<10){
		next;
	}else{
		#my $green_col=int(($idPct-80)/20*255);
		my $green_col=int((100-$idPct)/20*255);
		my $dotcol='rgb(255,'.$green_col.',0)';
		if($idPct<80){
            $dotcol="darkgray";
        }
		if($idPct>80){
			$dotcol="darkblue";
		}
		if($idPct>85){
			$dotcol="darkslateblue";
		}	
		if($idPct>89){
			$dotcol="cornflowerblue";
		}
		if($idPct>91.5){
			$dotcol="greenyellow";
		}
		if($idPct>92){
			$dotcol="yellow";
		}
		if($idPct>92.5){
			$dotcol="gold";
		}
		if($idPct>93){
			$dotcol="orange";
		}
		if($idPct>95){
			$dotcol="orangered";
		}
		if($idPct>97){
			$dotcol="red";
		}
		if($idPct>99){
			$dotcol="firebrick";
		}
		if($start2 < $start1){
			if($strand2 eq "-"){
				$dotcol="blue";
			}else{
				$dotcol="red";
			}
		}
		if($strand2 eq "-"){
			my $a=$end1;
			my $b=$end2;
			my $c=$start1;
			my $d=$start2;
			$start1=$c;
			$start2=$b;
			$end1=$a;
			$end2=$d;
		}	
		$svg -> line(x1=> $x_left_margin+(($start1-$x_chr_start)/1000)*$Xpx_per_kb, 
			y1=> $Y-$y_bottom_margin-(($start2-$y_chr_start)/1000)*$Ypx_per_kb,
			x2=> $x_left_margin+(($end1-$x_chr_start)/1000)*$Xpx_per_kb,
			y2=> $Y-$y_bottom_margin-(($end2-$y_chr_start)/1000)*$Ypx_per_kb,
			style=>{
				'stroke'=>$dotcol,'opacity'=>'1',"stroke-width"=>1});
	}
}

my $flanking_size=shift;
draw_single_track($x_chr_start,$x_chr_start+$flanking_size,$y_bottom_margin,($flanking_size/1000)*$Xpx_per_kb,"gray");
draw_single_track($x_chr_end-$flanking_size, $x_chr_end, $y_bottom_margin,($flanking_size/1000)*$Xpx_per_kb,"gray");
draw_single_track($x_chr_start,$x_chr_start+$flanking_size,$Y-$y_bottom_margin-($flanking_size/1000)*$Xpx_per_kb,($flanking_size/1000)*$Xpx_per_kb,"gray");
draw_single_track($x_chr_end-$flanking_size, $x_chr_end, $Y-$y_bottom_margin-($flanking_size/1000)*$Xpx_per_kb,($flanking_size/1000)*$Xpx_per_kb,"gray");

my $nfile=shift;
if(-e $nfile){
	open(FN,$nfile);
	while(<FN>){
		chomp;
		(my $chr,my $start,my $end, my $type)=split(/\s+/,$_);
		next if($type eq "SEQ");
		next if($chr ne $chr1);
		my $x1=$x_left_margin+(($start-$x_chr_start)/1000)*$Xpx_per_kb;
		my $y1=$Y-$y_bottom_margin-(($start-$y_chr_start)/1000)*$Ypx_per_kb;
		#vertical
		$svg -> line(x1=> $x1, 
			y1=> $y_bottom_margin,
			x2=> $x1,
			y2=> $Y-$y_bottom_margin,
			style=>{
				'stroke'=>'black','opacity'=>'1',"stroke-width"=>2});
		#horizontal
		$svg -> line(x1=> $x_left_margin, 
			y1=> $y1,
			x2=> $X-$x_left_margin-$x_right_margin,
			y2=> $y1,
			style=>{
				'stroke'=>'black','opacity'=>'1',"stroke-width"=>2});
	}
}

my $bin=$bin_size;
for(my $i=0;$i*$bin<$total_x_chr;$i++){
	 my $yp=$Y-$y_bottom_margin;
	 my $x2=($i*$bin)/1000*$Xpx_per_kb+$x_left_margin;
	 if($i%10 == 0){
		 my $te=int(($i*$bin+$x_chr_start)/$bin);
		 $svg->text(x=>$x2-3,y=>$yp+10,
		 width=>5,height=>5,"font-family"=>"Arial",
		 "textanchor"=>"start","font-size"=>16,"-cdata"=>"$te ");		
		 $svg -> line(x1=> $x2, y1=>$yp ,
		x2=> $x2,y2=> $yp+5,
		 style=>{
		 'stroke'=>'black','opacity'=>'1',"stroke-width"=>0.8});
	 }
	$svg -> line(x1=> $x2, y1=>$yp ,
	x2=> $x2,y2=> $yp+3,
	style=>{
		'stroke'=>'black','opacity'=>'1',"stroke-width"=>0.4});	
	# $svg -> line(x1=> $chr_w_axis, y1=>$yp ,
		# x2=> $x2d,y2=> $yp,
		# style=>{
		# 'stroke'=>'black','opacity'=>'1',"stroke-width"=>0.8});
}
# $bin=10;

my $out=$svg->xmlify;

open(SVGFILE, ">$outname")||die $!;
print SVGFILE $out;		
	


sub draw_triangle{
	my($x,$y,$svg) = @_;
	my $xv = [$x,$x+10,$x+10];
	my $yv = [$y,$y-3,$y+3];
	my $points = $svg -> get_path(
        x=>$xv, y=>$yv,
        -type=>'polygon'
    );
	$svg ->polygon(
        %$points,
        style=>{
		'stroke'=>'black','opacity'=>'1','fill'=>'white',
		'fill-opacity'=>'0',"stroke-width"=>1.5});
}


sub draw_single_track{
	my($start,$end,$track_y,$height,$color) = @_;
	my $x = (($start-$x_chr_start)/1000)*$Xpx_per_kb;
	my $x2 = (($end-$x_chr_start)/1000)*$Xpx_per_kb;
	my $ttbox_w=$x2-$x;
	#print $ttbox_w,"\n";
	if($ttbox_w<1){
		$ttbox_w=1;
	}
	$svg->rect(x=>$x_left_margin+$x,y=>$track_y, width=>$ttbox_w,height=>$height,
           rx    => 0, ry     =>0,
		   style=>{'stroke'=>$color,'opacity'=>'0.2','fill'=>$color,
		   'stroke-width'=>'0.5'}
		   );
}

