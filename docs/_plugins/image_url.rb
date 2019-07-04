module Jekyll
  module BaseUrlFilter
    def image_url(input, width=256)
      site = @context.registers[:site].config
      image_baseurl = site['image_baseurl']
      baseurl = site['baseurl']
      "#{image_baseurl}#{baseurl}/discography/#{input}.ptif/full/#{width},/0/default.jpg"
    end
  end
end

Liquid::Template.register_filter(Jekyll::BaseUrlFilter)
