<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="0" version="3.14.1-Pi" simplifyDrawingTol="1" readOnly="0" maxScale="0" labelsEnabled="0" minScale="100000000" simplifyAlgorithm="0" simplifyLocal="1" styleCategories="AllStyleCategories" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal mode="0" endField="" startExpression="" startField="" fixedDuration="0" durationUnit="min" endExpression="" durationField="" enabled="0" accumulate="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="RuleRenderer" enableorderby="0" symbollevels="0" forceraster="0">
    <rules key="{803f935d-d6de-4386-8143-af55ce9070fe}">
      <rule label="parallel on_street" key="{77c31a18-3b85-43ed-9ced-853f1c8c7389}" symbol="0" filter="&quot;orientation&quot; = 'parallel' AND ((&quot;position&quot; != 'half_on_kerb' AND &quot;position&quot; != 'on_kerb' AND &quot;position&quot; != 'shoulder' AND &quot;position&quot; != 'street_side' AND &quot;position&quot; != 'lay_by') OR &quot;position&quot; IS NULL)"/>
      <rule label="parallel half_on_kerb" key="{dde9ac74-a9ea-4202-8779-fc7d314b2961}" symbol="1" filter="&quot;orientation&quot; = 'parallel' AND &quot;position&quot; = 'half_on_kerb'"/>
      <rule label="parallel on_kerb/shoulder/street_side/lay_by" key="{7ad919ba-f76a-4074-94b8-dc3f4ad60bfb}" symbol="2" filter="&quot;orientation&quot; = 'parallel' AND (&quot;position&quot; = 'on_kerb' OR &quot;position&quot; = 'shoulder' OR &quot;position&quot; = 'street_side' OR &quot;position&quot; = 'lay_by')"/>
      <rule label="diagonal on_street" key="{469dcfde-eeb7-4d8e-b3ca-f21c5dc77aad}" symbol="3" filter="&quot;orientation&quot; = 'diagonal' AND ((&quot;position&quot; != 'half_on_kerb' AND &quot;position&quot; != 'on_kerb' AND &quot;position&quot; != 'shoulder' AND &quot;position&quot; != 'street_side' AND &quot;position&quot; != 'lay_by') OR &quot;position&quot; IS NULL)"/>
      <rule label="diagonal half_on_kerb" key="{ffa64ff1-13ff-4dcd-a7a5-6cad92c48063}" symbol="4" filter="&quot;orientation&quot; = 'diagonal' AND &quot;position&quot; = 'half_on_kerb'"/>
      <rule label="diagonal on_kerb/shoulder/street_side/lay_by" key="{c7e5b9c2-2e94-4ac0-87b7-7cf0903d0507}" symbol="5" filter="&quot;orientation&quot; = 'diagonal' AND (&quot;position&quot; = 'on_kerb' OR &quot;position&quot; = 'shoulder' OR &quot;position&quot; = 'street_side' OR &quot;position&quot; = 'lay_by')"/>
      <rule label="perpendicular on_street" key="{2cc6da87-6460-4565-9d0a-1f9463f535bb}" symbol="6" filter="&quot;orientation&quot; = 'perpendicular' AND ((&quot;position&quot; != 'half_on_kerb' AND &quot;position&quot; != 'on_kerb' AND &quot;position&quot; != 'shoulder' AND &quot;position&quot; != 'street_side' AND &quot;position&quot; != 'lay_by') OR &quot;position&quot; IS NULL)"/>
      <rule label="perpendicular half_on_kerb" key="{2cc6da87-6460-4565-9d0a-1f9463f535bb}" symbol="7" filter="&quot;orientation&quot; = 'perpendicular' AND &quot;position&quot; = 'half_on_kerb'"/>
      <rule label="perpendicular on_kerb/shoulder/street_side/lay_by" key="{1387d40f-c62f-417f-a213-7442061b9203}" symbol="8" filter="&quot;orientation&quot; = 'perpendicular' AND (&quot;position&quot; = 'on_kerb' OR &quot;position&quot; = 'shoulder' OR &quot;position&quot; = 'street_side' OR &quot;position&quot; = 'lay_by')"/>
    </rules>
    <symbols>
      <symbol name="0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="90"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="1.1"/>
          <prop k="offset_along_line" v="2.2"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="1" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="90"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="1.1"/>
          <prop k="offset_along_line" v="2.2"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="1.1"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="2" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="90"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="1.1"/>
          <prop k="offset_along_line" v="2.2"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@2@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="2.2"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="3" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="324"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="3.1"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MapUnit"/>
          <prop k="offset" v="2.2"/>
          <prop k="offset_along_line" v="3.1"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@3@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="4" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="144"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="3.1"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MapUnit"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="3.1"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@4@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="5" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="144"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="3.1"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MapUnit"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="3.1"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="3.1"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="6" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="0"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="2.5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="2.2"/>
          <prop k="offset_along_line" v="1.1"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@6@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="6,34,172,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="7" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="0"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="2.5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="1.1"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@7@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="6,34,172,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="8" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer locked="0" pass="0" class="HashLine" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="0"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="2.5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="-2.2"/>
          <prop k="offset_along_line" v="1.1"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@8@0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
            <layer locked="0" pass="0" class="SimpleLine" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="6,34,172,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions" value="&quot;highway:name&quot;"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory direction="0" labelPlacementMethod="XHeight" opacity="1" height="15" maxScaleDenominator="1e+8" barWidth="5" penWidth="0" penColor="#000000" spacingUnit="MM" sizeScale="3x:0,0,0,0,0,0" spacingUnitScale="3x:0,0,0,0,0,0" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" minScaleDenominator="0" width="15" scaleDependency="Area" lineSizeType="MM" sizeType="MM" penAlpha="255" minimumSize="0" rotationOffset="270" diagramOrientation="Up" scaleBasedVisibility="0" backgroundColor="#ffffff" spacing="5" backgroundAlpha="255" showAxis="1">
      <fontProperties style="" description="Cantarell,11,-1,5,50,0,0,0,0,0"/>
      <attribute field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol name="" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
          <layer locked="0" pass="0" class="SimpleLine" enabled="1">
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="18" zIndex="0" placement="2" obstacle="0" showAll="1" priority="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <referencedLayers/>
  <referencingLayers/>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:width_proc">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:width_proc:effective">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="error_output">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="orientation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="position">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition:other">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition:other:time">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxstay">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="source:capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="offset">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="layer">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="path">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="highway" index="1"/>
    <alias name="" field="highway:name" index="2"/>
    <alias name="" field="highway:width_proc" index="3"/>
    <alias name="" field="highway:width_proc:effective" index="4"/>
    <alias name="" field="error_output" index="5"/>
    <alias name="" field="parking" index="6"/>
    <alias name="" field="orientation" index="7"/>
    <alias name="" field="position" index="8"/>
    <alias name="" field="condition" index="9"/>
    <alias name="" field="condition:other" index="10"/>
    <alias name="" field="condition:other:time" index="11"/>
    <alias name="" field="maxstay" index="12"/>
    <alias name="" field="capacity" index="13"/>
    <alias name="" field="source:capacity" index="14"/>
    <alias name="" field="width" index="15"/>
    <alias name="" field="offset" index="16"/>
    <alias name="" field="layer" index="17"/>
    <alias name="" field="path" index="18"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="highway" applyOnUpdate="0"/>
    <default expression="" field="highway:name" applyOnUpdate="0"/>
    <default expression="" field="highway:width_proc" applyOnUpdate="0"/>
    <default expression="" field="highway:width_proc:effective" applyOnUpdate="0"/>
    <default expression="" field="error_output" applyOnUpdate="0"/>
    <default expression="" field="parking" applyOnUpdate="0"/>
    <default expression="" field="orientation" applyOnUpdate="0"/>
    <default expression="" field="position" applyOnUpdate="0"/>
    <default expression="" field="condition" applyOnUpdate="0"/>
    <default expression="" field="condition:other" applyOnUpdate="0"/>
    <default expression="" field="condition:other:time" applyOnUpdate="0"/>
    <default expression="" field="maxstay" applyOnUpdate="0"/>
    <default expression="" field="capacity" applyOnUpdate="0"/>
    <default expression="" field="source:capacity" applyOnUpdate="0"/>
    <default expression="" field="width" applyOnUpdate="0"/>
    <default expression="" field="offset" applyOnUpdate="0"/>
    <default expression="" field="layer" applyOnUpdate="0"/>
    <default expression="" field="path" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" field="id" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="highway" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="highway:name" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="highway:width_proc" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="highway:width_proc:effective" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="error_output" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="parking" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="orientation" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="position" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="condition" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="condition:other" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="condition:other:time" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="maxstay" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="capacity" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="source:capacity" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="width" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="offset" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="layer" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="path" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" exp="" desc=""/>
    <constraint field="highway" exp="" desc=""/>
    <constraint field="highway:name" exp="" desc=""/>
    <constraint field="highway:width_proc" exp="" desc=""/>
    <constraint field="highway:width_proc:effective" exp="" desc=""/>
    <constraint field="error_output" exp="" desc=""/>
    <constraint field="parking" exp="" desc=""/>
    <constraint field="orientation" exp="" desc=""/>
    <constraint field="position" exp="" desc=""/>
    <constraint field="condition" exp="" desc=""/>
    <constraint field="condition:other" exp="" desc=""/>
    <constraint field="condition:other:time" exp="" desc=""/>
    <constraint field="maxstay" exp="" desc=""/>
    <constraint field="capacity" exp="" desc=""/>
    <constraint field="source:capacity" exp="" desc=""/>
    <constraint field="width" exp="" desc=""/>
    <constraint field="offset" exp="" desc=""/>
    <constraint field="layer" exp="" desc=""/>
    <constraint field="path" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="&quot;id&quot;">
    <columns>
      <column name="id" type="field" hidden="0" width="271"/>
      <column name="highway" type="field" hidden="0" width="-1"/>
      <column name="highway:name" type="field" hidden="0" width="-1"/>
      <column name="error_output" type="field" hidden="0" width="-1"/>
      <column name="parking" type="field" hidden="0" width="-1"/>
      <column name="position" type="field" hidden="0" width="-1"/>
      <column name="condition" type="field" hidden="0" width="-1"/>
      <column name="condition:other" type="field" hidden="0" width="-1"/>
      <column name="condition:other:time" type="field" hidden="0" width="-1"/>
      <column name="maxstay" type="field" hidden="0" width="-1"/>
      <column name="capacity" type="field" hidden="0" width="-1"/>
      <column name="width" type="field" hidden="0" width="-1"/>
      <column name="offset" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
      <column name="highway:width_proc" type="field" hidden="0" width="-1"/>
      <column name="highway:width_proc:effective" type="field" hidden="0" width="-1"/>
      <column name="orientation" type="field" hidden="0" width="-1"/>
      <column name="source:capacity" type="field" hidden="0" width="-1"/>
      <column name="layer" type="field" hidden="0" width="-1"/>
      <column name="path" type="field" hidden="0" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="capacity" editable="1"/>
    <field name="condition" editable="1"/>
    <field name="condition:other" editable="1"/>
    <field name="condition:other:time" editable="1"/>
    <field name="error_output" editable="1"/>
    <field name="highway" editable="1"/>
    <field name="highway:name" editable="1"/>
    <field name="highway:width" editable="1"/>
    <field name="highway:width:effective" editable="1"/>
    <field name="highway:width_proc" editable="1"/>
    <field name="highway:width_proc:effective" editable="1"/>
    <field name="id" editable="1"/>
    <field name="layer" editable="1"/>
    <field name="maxstay" editable="1"/>
    <field name="offset" editable="1"/>
    <field name="orientation" editable="1"/>
    <field name="parking" editable="1"/>
    <field name="path" editable="1"/>
    <field name="position" editable="1"/>
    <field name="source:capacity" editable="1"/>
    <field name="width" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="capacity" labelOnTop="0"/>
    <field name="condition" labelOnTop="0"/>
    <field name="condition:other" labelOnTop="0"/>
    <field name="condition:other:time" labelOnTop="0"/>
    <field name="error_output" labelOnTop="0"/>
    <field name="highway" labelOnTop="0"/>
    <field name="highway:name" labelOnTop="0"/>
    <field name="highway:width" labelOnTop="0"/>
    <field name="highway:width:effective" labelOnTop="0"/>
    <field name="highway:width_proc" labelOnTop="0"/>
    <field name="highway:width_proc:effective" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="layer" labelOnTop="0"/>
    <field name="maxstay" labelOnTop="0"/>
    <field name="offset" labelOnTop="0"/>
    <field name="orientation" labelOnTop="0"/>
    <field name="parking" labelOnTop="0"/>
    <field name="path" labelOnTop="0"/>
    <field name="position" labelOnTop="0"/>
    <field name="source:capacity" labelOnTop="0"/>
    <field name="width" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"highway:name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
